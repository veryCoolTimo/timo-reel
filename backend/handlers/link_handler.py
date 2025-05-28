import re
import logging
from urllib.parse import urlparse, parse_qs
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from downloader.video_downloader import downloader
from utils.cache import add_video_metadata

logger = logging.getLogger(__name__)

# Регулярные выражения для поиска ссылок
URL_PATTERNS = [
    # Instagram
    r'https?://(?:www\.)?instagram\.com/(?:p|reel|tv)/([A-Za-z0-9_-]+)/?',
    r'https?://(?:www\.)?instagram\.com/stories/[^/]+/(\d+)/?',
    
    # TikTok
    r'https?://(?:www\.)?tiktok\.com/@[^/]+/video/(\d+)',
    r'https?://(?:vm|vt)\.tiktok\.com/([A-Za-z0-9]+)/?',
    r'https?://(?:www\.)?tiktok\.com/t/([A-Za-z0-9]+)/?',
]

def normalize_url(url: str) -> str:
    """Нормализует URL, убирая параметры запроса и лишние символы"""
    try:
        parsed = urlparse(url)
        # Убираем параметры запроса и фрагменты
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        # Убираем завершающий слеш если он есть
        if normalized.endswith('/'):
            normalized = normalized[:-1]
        return normalized
    except:
        return url

def extract_urls_from_text(text: str) -> list[str]:
    """Извлекает все поддерживаемые URL из текста с дедупликацией"""
    urls = []
    normalized_urls = set()  # Для отслеживания уже найденных URL
    
    for pattern in URL_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            url = match.group(0)
            normalized = normalize_url(url)
            
            # Добавляем только если еще не встречали такой URL
            if normalized not in normalized_urls:
                urls.append(url)
                normalized_urls.add(normalized)
    
    # Также ищем любые URL, содержащие поддерживаемые домены
    general_url_pattern = r'https?://[^\s]+'
    general_matches = re.finditer(general_url_pattern, text, re.IGNORECASE)
    
    for match in general_matches:
        url = match.group(0)
        normalized = normalize_url(url)
        
        if (downloader.is_supported_url(url) and 
            normalized not in normalized_urls):
            urls.append(url)
            normalized_urls.add(normalized)
    
    return urls

async def handle_message_with_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает сообщения, содержащие ссылки на видео"""
    if not update.message or not update.message.text:
        return
    
    message = update.message
    chat_id = message.chat_id
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Извлекаем URL из сообщения с дедупликацией
    urls = extract_urls_from_text(message.text)
    
    if not urls:
        return
    
    logger.info(f"Found {len(urls)} unique video URLs in message from user {user_id}")
    
    # Дополнительная проверка на дубликаты по нормализованным URL
    processed_urls = set()
    
    for url in urls:
        normalized_url = normalize_url(url)
        
        # Пропускаем если уже обрабатывали такой URL
        if normalized_url in processed_urls:
            logger.info(f"Skipping duplicate URL: {url}")
            continue
        
        processed_urls.add(normalized_url)
        
        try:
            # Показываем, что бот печатает
            await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_VIDEO)
            
            # Сначала проверяем информацию о видео
            video_info = downloader.extract_info(url)
            if not video_info:
                logger.warning(f"Could not extract info from URL: {url}")
                
                # Определяем тип ошибки по платформе
                if 'instagram.com' in url:
                    error_msg = (
                        f"❌ Не удалось загрузить видео из Instagram\n\n"
                        f"🔒 Возможные причины:\n"
                        f"• Видео приватное или удалено\n"
                        f"• Instagram блокирует автоматические запросы\n"
                        f"• Аккаунт заблокирован или требует входа\n\n"
                        f"💡 Попробуйте:\n"
                        f"• Убедиться, что видео публичное\n"
                        f"• Попробовать другую ссылку\n"
                        f"• Повторить попытку через несколько минут"
                    )
                elif 'tiktok.com' in url or 'vm.tiktok.com' in url:
                    error_msg = (
                        f"❌ Не удалось загрузить видео из TikTok\n\n"
                        f"🔒 Возможные причины:\n"
                        f"• Видео приватное или удалено\n"
                        f"• Географические ограничения\n"
                        f"• Временная блокировка TikTok\n\n"
                        f"💡 Попробуйте другую ссылку или повторите позже"
                    )
                else:
                    error_msg = f"❌ Не удалось загрузить видео из {url}\nПопробуйте другую ссылку"
                
                await message.reply_text(error_msg)
                continue
            
            logger.info(f"Downloading video: {video_info['title']} from {url}")
            
            # Отправляем сообщение о начале загрузки
            status_message = await message.reply_text(
                f"⬇️ Загружаю видео...\n"
                f"📹 {video_info['title'][:50]}{'...' if len(video_info['title']) > 50 else ''}\n"
                f"👤 {video_info['uploader']}"
            )
            
            # Загружаем видео
            video_path = downloader.download_video(url)
            if not video_path:
                await status_message.edit_text(
                    f"❌ Не удалось загрузить видео\n\n"
                    f"🔍 Проверьте:\n"
                    f"• Видео не превышает 50MB\n"
                    f"• Ссылка корректная и публичная\n"
                    f"• Видео не удалено автором\n\n"
                    f"💡 Попробуйте другую ссылку или повторите позже"
                )
                continue
            
            try:
                # Обновляем статус
                await status_message.edit_text("📤 Отправляю видео...")
                
                # Отправляем видео в чат
                with open(video_path, 'rb') as video_file:
                    sent_message = await context.bot.send_video(
                        chat_id=chat_id,
                        video=video_file,
                        caption=f"🎬 {video_info['title']}\n👤 @{username}",
                        reply_to_message_id=message.message_id,
                        supports_streaming=True
                    )
                
                # Удаляем статусное сообщение
                await status_message.delete()
                
                # Сохраняем метаданные
                if sent_message.video:
                    file_id = sent_message.video.file_id
                    add_video_metadata(
                        file_id=file_id,
                        chat_id=chat_id,
                        user_id=user_id,
                        username=username
                    )
                    logger.info(f"Video saved with file_id: {file_id}")
                
            finally:
                # Очищаем временный файл
                downloader.cleanup_file(video_path)
                
        except Exception as e:
            logger.error(f"Error processing URL {url}: {e}")
            
            # Определяем тип ошибки для пользователя
            if "File too large" in str(e) or "too large" in str(e).lower():
                error_msg = (
                    f"❌ Видео слишком большое (>50MB)\n\n"
                    f"📏 Ограничения Telegram:\n"
                    f"• Максимальный размер: 50MB\n"
                    f"• Попробуйте найти видео меньшего размера"
                )
            elif "Network" in str(e) or "timeout" in str(e).lower():
                error_msg = (
                    f"❌ Проблема с сетью\n\n"
                    f"🌐 Проверьте подключение к интернету\n"
                    f"🔄 Попробуйте еще раз через минуту"
                )
            else:
                error_msg = (
                    f"❌ Произошла ошибка при обработке видео\n\n"
                    f"🔧 Попробуйте:\n"
                    f"• Проверить ссылку\n"
                    f"• Повторить попытку\n"
                    f"• Использовать другую ссылку"
                )
            
            await message.reply_text(error_msg)

async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех текстовых сообщений для поиска ссылок"""
    await handle_message_with_links(update, context) 