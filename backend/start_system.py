#!/usr/bin/env python3
"""
Скрипт для запуска всей системы TimoReel
Запускает бота и API сервер одновременно
"""

import asyncio
import logging
import signal
import sys
from concurrent.futures import ThreadPoolExecutor

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def run_bot():
    """Запускает Telegram бота"""
    try:
        from bot import main as bot_main
        logger.info("Starting Telegram Bot...")
        await bot_main()
    except Exception as e:
        logger.error(f"Bot error: {e}")
        raise

async def run_api_server():
    """Запускает API сервер"""
    try:
        from api_server import main as api_main
        logger.info("Starting API Server...")
        await api_main()
    except Exception as e:
        logger.error(f"API Server error: {e}")
        raise

async def main():
    """Основная функция - запускает бота и API сервер параллельно"""
    logger.info("🚀 Starting TimoReel System...")
    
    # Создаем задачи для бота и API сервера
    tasks = [
        asyncio.create_task(run_bot(), name="telegram_bot"),
        asyncio.create_task(run_api_server(), name="api_server")
    ]
    
    try:
        # Запускаем обе задачи параллельно
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down TimoReel System...")
        
        # Отменяем все задачи
        for task in tasks:
            if not task.done():
                task.cancel()
        
        # Ждем завершения отмены
        await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info("✅ TimoReel System stopped")

def signal_handler(signum, frame):
    """Обработчик сигналов для корректного завершения"""
    logger.info(f"Received signal {signum}")
    sys.exit(0)

if __name__ == '__main__':
    # Устанавливаем обработчики сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("System stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1) 