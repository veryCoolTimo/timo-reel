#!/usr/bin/env python3
"""
Простой тестовый бот для проверки токена
"""

import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from utils.config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "🎬 Привет! Я TimoReel бот!\n\n"
        "✅ Бот работает!\n"
        "✅ Токен корректный!\n"
        "✅ Команды обрабатываются!\n\n"
        "Отправьте /help для получения помощи."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "🆘 Помощь по TimoReel Bot\n\n"
        "📋 Доступные команды:\n"
        "/start - приветствие\n"
        "/help - эта помощь\n"
        "/test - тест бота\n\n"
        "📝 Функции:\n"
        "• Автоматическое скачивание видео из Instagram и TikTok\n"
        "• Просто отправьте ссылку на видео!"
    )

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Тестовая команда"""
    user = update.effective_user
    chat = update.effective_chat
    
    await update.message.reply_text(
        f"🧪 Тест бота\n\n"
        f"👤 Пользователь: {user.first_name} (@{user.username})\n"
        f"💬 Чат: {chat.title or 'Личные сообщения'}\n"
        f"🆔 Chat ID: {chat.id}\n"
        f"🆔 User ID: {user.id}\n\n"
        f"✅ Все работает отлично!"
    )

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Эхо для всех сообщений"""
    text = update.message.text
    
    # Проверяем, есть ли ссылки
    if 'instagram.com' in text or 'tiktok.com' in text or 'vm.tiktok.com' in text:
        await update.message.reply_text(
            "🔗 Обнаружена ссылка на видео!\n\n"
            "⚠️ Функция скачивания пока не активна.\n"
            "Это будет реализовано в следующих этапах."
        )
    else:
        await update.message.reply_text(
            f"📝 Получено сообщение: {text}\n\n"
            "Отправьте ссылку на Instagram или TikTok для скачивания видео!"
        )

async def main():
    """Основная функция"""
    logger.info("🚀 Starting Simple TimoReel Bot...")
    
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не установлен!")
        return
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("test", test_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    
    logger.info("✅ Bot handlers configured")
    logger.info("🔄 Starting polling...")
    
    # Запускаем polling
    async with application:
        await application.start()
        await application.updater.start_polling(drop_pending_updates=True)
        
        logger.info("🎉 Bot started successfully!")
        logger.info("📱 Send /start to the bot to test it")
        logger.info("🛑 Press Ctrl+C to stop")
        
        try:
            # Ждем сигнала остановки
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Bot stopped by user")
        finally:
            await application.updater.stop()
            await application.stop()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Goodbye!")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        import traceback
        traceback.print_exc() 