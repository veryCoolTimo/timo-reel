#!/usr/bin/env python3
"""
TimoReel System Launcher
Запускает бота и API сервер одновременно
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импортов
sys.path.insert(0, str(Path(__file__).parent))

from utils.config import BOT_TOKEN
from bot import create_application
from api_server import create_api_app
from aiohttp import web

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def check_environment():
    """Проверяет настройки окружения"""
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не установлен!")
        logger.error("Создайте файл backend/.env со следующим содержимым:")
        logger.error("BOT_TOKEN=your_telegram_bot_token_here")
        logger.error("")
        logger.error("Получить токен можно у @BotFather в Telegram:")
        logger.error("1. Напишите /newbot")
        logger.error("2. Выберите имя и username для бота")
        logger.error("3. Скопируйте полученный токен в .env файл")
        return False
    
    # Проверяем директории
    storage_dir = Path(__file__).parent / "storage"
    storage_dir.mkdir(exist_ok=True)
    
    return True

async def start_api_server():
    """Запускает API сервер"""
    try:
        app = create_api_app()
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, '0.0.0.0', 8001)
        await site.start()
        
        logger.info("✅ API Server started on http://0.0.0.0:8001")
        return runner
    except Exception as e:
        logger.error(f"❌ Failed to start API server: {e}")
        raise

async def start_telegram_bot():
    """Запускает Telegram бота"""
    try:
        application = create_application()
        
        # Запускаем polling
        logger.info("✅ Starting Telegram Bot with polling...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling(
            allowed_updates=['message', 'callback_query'],
            drop_pending_updates=True
        )
        
        logger.info("✅ Telegram Bot started successfully!")
        return application
    except Exception as e:
        logger.error(f"❌ Failed to start Telegram bot: {e}")
        raise

async def main():
    """Основная функция запуска системы"""
    logger.info("🚀 Starting TimoReel System...")
    
    # Проверяем окружение
    if not check_environment():
        return
    
    try:
        # Запускаем API сервер
        api_runner = await start_api_server()
        
        # Запускаем Telegram бота
        bot_app = await start_telegram_bot()
        
        logger.info("🎉 TimoReel System started successfully!")
        logger.info("📱 Bot is ready to receive messages")
        logger.info("🌐 API Server: http://localhost:8001")
        logger.info("🎬 WebApp: http://localhost:3000 (run 'npm run dev' in webapp/)")
        logger.info("")
        logger.info("Press Ctrl+C to stop...")
        
        # Ждем сигнала остановки
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Stopping TimoReel System...")
            
            # Останавливаем бота
            await bot_app.updater.stop()
            await bot_app.stop()
            await bot_app.shutdown()
            
            # Останавливаем API сервер
            await api_runner.cleanup()
            
            logger.info("✅ TimoReel System stopped")
            
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Goodbye!")
    except Exception as e:
        logger.error(f"💥 System crashed: {e}")
        sys.exit(1) 