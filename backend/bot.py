#!/usr/bin/env python3
"""
TimoReel Telegram Bot
Автоматически скачивает видео из Instagram и TikTok
"""

import logging
import asyncio
from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters,
    ContextTypes
)
from utils.config import BOT_TOKEN, HOST, PORT, WEBHOOK_URL, WEBHOOK_PATH
from handlers.link_handler import handle_all_messages
from handlers.pm_commands import mute_command, unmute_command, likes_command, status_command

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    if update.message.chat.type == 'private':
        # В личных сообщениях показываем расширенную информацию
        welcome_text = f"""
🎬 Привет, {user.first_name}!

Я TimoReel бот - автоматически скачиваю видео из Instagram и TikTok!

📝 Как пользоваться:
• Добавь меня в групповой чат
• Отправь ссылку на видео из Instagram или TikTok
• Я автоматически скачаю и отправлю видео в чат
• Все видео сохраняются в ленте для просмотра в WebApp

🔗 Поддерживаемые ссылки:
• Instagram: посты, reels, stories
• TikTok: обычные видео и короткие ссылки

⚙️ Команды в личных сообщениях:
/start - показать это сообщение
/help - подробная помощь
/status - ваш статус и статистика
/mute - отключить уведомления о реакциях
/unmute - включить уведомления о реакциях
/likes - показать историю ваших реакций

Добавь меня в чат и отправь ссылку! 🚀
"""
    else:
        # В групповых чатах краткая информация
        welcome_text = f"""
🎬 Привет! Я TimoReel бот!

Отправьте ссылку на видео из Instagram или TikTok, и я автоматически скачаю его для вас.

Поддерживаемые платформы: Instagram, TikTok
Используйте /help для подробной информации.
"""
    
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
🆘 Помощь по TimoReel Bot

📋 Основные функции:
• Автоматическое скачивание видео из Instagram и TikTok
• Сохранение в ленте для просмотра в WebApp
• Система лайков и комментариев

🔗 Поддерживаемые форматы ссылок:

Instagram:
• https://instagram.com/p/ABC123/
• https://instagram.com/reel/ABC123/
• https://instagram.com/tv/ABC123/

TikTok:
• https://tiktok.com/@user/video/123456
• https://vm.tiktok.com/ABC123/
• https://vt.tiktok.com/ABC123/

⚠️ Ограничения:
• Максимальный размер видео: 50MB
• Только публичные видео
• Некоторые видео могут быть недоступны из-за настроек приватности

❓ Проблемы?
Если видео не загружается, проверьте:
1. Ссылка корректная и публичная
2. Видео не превышает 50MB
3. Аккаунт не заблокирован

Просто отправьте ссылку в чат! 🎬
"""
    await update.message.reply_text(help_text)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Exception while handling an update: {context.error}")
    
    # Если есть update и это сообщение, отправляем уведомление пользователю
    if isinstance(update, Update) and update.message:
        await update.message.reply_text(
            "❌ Произошла ошибка при обработке вашего запроса. "
            "Попробуйте еще раз или обратитесь к администратору."
        )

def create_application() -> Application:
    """Создает и настраивает приложение бота"""
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не установлен! Проверьте файл .env")
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Команды для личных сообщений
    application.add_handler(CommandHandler("mute", mute_command))
    application.add_handler(CommandHandler("unmute", unmute_command))
    application.add_handler(CommandHandler("likes", likes_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # Добавляем обработчик всех текстовых сообщений для поиска ссылок
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages)
    )
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    return application

async def main():
    """Основная функция запуска бота"""
    logger.info("Starting TimoReel Bot...")
    
    # Создаем приложение
    application = create_application()
    
    if WEBHOOK_URL:
        # Запуск с webhook (для production)
        logger.info(f"Starting webhook on {WEBHOOK_URL}{WEBHOOK_PATH}")
        await application.run_webhook(
            listen=HOST,
            port=PORT,
            webhook_url=f"{WEBHOOK_URL}{WEBHOOK_PATH}",
            url_path=WEBHOOK_PATH
        )
    else:
        # Запуск с polling (для разработки)
        logger.info("Starting polling...")
        await application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise 