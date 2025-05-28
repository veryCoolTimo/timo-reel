#!/usr/bin/env python3
"""
TimoReel API Server
Обрабатывает запросы от WebApp
"""

import logging
import asyncio
from aiohttp import web
from utils.config import HOST, PORT
from handlers.webapp_handler import create_webapp

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def create_api_app():
    """Создает API приложение для использования в start_system.py"""
    return await create_webapp()

async def main():
    """Основная функция запуска API сервера"""
    logger.info("Starting TimoReel API Server...")
    
    # Создаем веб-приложение
    app = await create_webapp()
    
    # Запускаем сервер
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Используем порт +1 от основного порта бота для API
    api_port = PORT + 1
    site = web.TCPSite(runner, HOST, api_port)
    await site.start()
    
    logger.info(f"API Server started on http://{HOST}:{api_port}")
    logger.info("Available endpoints:")
    logger.info(f"  GET  /api/health - Health check")
    logger.info(f"  GET  /api/feed?chat_id=<id> - Get video feed for chat")
    logger.info(f"  POST /api/react - Send reaction (like/comment)")
    logger.info(f"  GET  /api/video/<file_id> - Get video info")
    logger.info(f"  GET  /api/stats - Get general statistics")
    
    try:
        # Держим сервер запущенным
        while True:
            await asyncio.sleep(3600)  # Спим час
    except KeyboardInterrupt:
        logger.info("API Server stopped by user")
    finally:
        await runner.cleanup()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("API Server stopped")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise 