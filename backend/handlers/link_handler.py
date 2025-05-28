import re
import logging
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

def extract_urls_from_text(text: str) -> list[str]:
    """Извлекает все поддерживаемые URL из текста"""
    urls = []
    
    for pattern in URL_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            urls.append(match.group(0))
    
    # Также ищем любые URL, содержащие поддерживаемые домены
    general_url_pattern = r'https?://[^\s]+'
    general_matches = re.finditer(general_url_pattern, text, re.IGNORECASE)
    
    for match in general_matches:
        url = match.group(0)
        if downloader.is_supported_url(url) and url not in urls:
            urls.append(url)
    
    return urls

async def handle_message_with_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает сообщения, содержащие ссылки на видео"""
    if not update.message or not update.message.text:
        return
    
    message = update.message
    chat_id = message.chat_id
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Извлекаем URL из сообщения
    urls = extract_urls_from_text(message.text)
    
    if not urls:
        return
    
    logger.info(f"Found {len(urls)} video URLs in message from user {user_id}")
    
    for url in urls:
        try:
            # Показываем, что бот печатает
            await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_VIDEO)
            
            # Сначала проверяем информацию о видео
            video_info = downloader.extract_info(url)
            if not video_info:
                logger.warning(f"Could not extract info from URL: {url}")
                continue
            
            logger.info(f"Downloading video: {video_info['title']} from {url}")
            
            # Загружаем видео
            video_path = downloader.download_video(url)
            if not video_path:
                await message.reply_text(
                    f"❌ Не удалось загрузить видео из {url}\n"
                    f"Возможно, видео слишком большое или недоступно."
                )
                continue
            
            try:
                # Отправляем видео в чат
                with open(video_path, 'rb') as video_file:
                    sent_message = await context.bot.send_video(
                        chat_id=chat_id,
                        video=video_file,
                        caption=f"🎬 {video_info['title']}\n👤 @{username}",
                        reply_to_message_id=message.message_id
                    )
                
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
            await message.reply_text(
                f"❌ Произошла ошибка при обработке видео из {url}"
            )

async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех текстовых сообщений для поиска ссылок"""
    await handle_message_with_links(update, context) 