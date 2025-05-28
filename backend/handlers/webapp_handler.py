#!/usr/bin/env python3
"""
Обработчик запросов от WebApp
"""

import json
import logging
from aiohttp import web, web_request
from aiohttp.web_response import Response
from utils.cache import get_videos_for_chat, get_stats
from handlers.reaction_handler import process_reaction

logger = logging.getLogger(__name__)

async def health_check(request: web_request.Request) -> Response:
    """Health check endpoint"""
    return web.json_response({
        "status": "healthy",
        "service": "TimoReel API",
        "version": "1.0.0",
        "stage": "5 - Reaction Notifications"
    })

async def get_video_feed(request: web_request.Request) -> Response:
    """Получает ленту видео для указанного чата"""
    try:
        chat_id = request.query.get('chat_id')
        if not chat_id:
            return web.json_response(
                {"error": "chat_id parameter is required"}, 
                status=400
            )
        
        try:
            chat_id = int(chat_id)
        except ValueError:
            return web.json_response(
                {"error": "chat_id must be a valid integer"}, 
                status=400
            )
        
        # Получаем видео для чата
        videos = get_videos_for_chat(chat_id)
        
        logger.info(f"Feed requested for chat {chat_id}: {len(videos)} videos")
        
        return web.json_response({
            "videos": videos,
            "count": len(videos),
            "chat_id": chat_id
        })
        
    except Exception as e:
        logger.error(f"Error getting video feed: {e}")
        return web.json_response(
            {"error": "Internal server error"}, 
            status=500
        )

async def send_reaction(request: web_request.Request) -> Response:
    """Обрабатывает реакцию пользователя"""
    try:
        # Получаем данные из запроса
        data = await request.json()
        
        # Валидация обязательных полей
        required_fields = ['user_id', 'file_id', 'type']
        for field in required_fields:
            if field not in data:
                return web.json_response(
                    {"error": f"Missing required field: {field}"}, 
                    status=400
                )
        
        user_id = data['user_id']
        file_id = data['file_id']
        reaction_type = data['type']
        username = data.get('username')  # Опционально
        
        # Валидация типов данных
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return web.json_response(
                {"error": "user_id must be a valid integer"}, 
                status=400
            )
        
        if not isinstance(file_id, str) or not file_id.strip():
            return web.json_response(
                {"error": "file_id must be a non-empty string"}, 
                status=400
            )
        
        # Валидация типа реакции
        valid_types = ['like', 'comment']
        if reaction_type not in valid_types:
            return web.json_response(
                {"error": f"Invalid reaction type. Must be one of: {valid_types}"}, 
                status=400
            )
        
        # Обрабатываем реакцию
        success = await process_reaction(
            user_id=user_id,
            file_id=file_id,
            reaction_type=reaction_type,
            username=username
        )
        
        if success:
            logger.info(f"Reaction processed: {user_id} {reaction_type} {file_id}")
            return web.json_response({
                "success": True,
                "message": f"Reaction '{reaction_type}' processed successfully",
                "user_id": user_id,
                "file_id": file_id,
                "type": reaction_type
            })
        else:
            logger.warning(f"Failed to process reaction: {user_id} {reaction_type} {file_id}")
            return web.json_response(
                {"error": "Failed to process reaction"}, 
                status=500
            )
        
    except json.JSONDecodeError:
        return web.json_response(
            {"error": "Invalid JSON in request body"}, 
            status=400
        )
    except Exception as e:
        logger.error(f"Error processing reaction: {e}")
        return web.json_response(
            {"error": "Internal server error"}, 
            status=500
        )

async def get_video_info(request: web_request.Request) -> Response:
    """Получает информацию о конкретном видео"""
    try:
        file_id = request.match_info.get('file_id')
        if not file_id:
            return web.json_response(
                {"error": "file_id is required"}, 
                status=400
            )
        
        # Здесь можно добавить логику получения детальной информации о видео
        # Пока возвращаем базовую информацию
        return web.json_response({
            "file_id": file_id,
            "message": "Video info endpoint - to be implemented"
        })
        
    except Exception as e:
        logger.error(f"Error getting video info: {e}")
        return web.json_response(
            {"error": "Internal server error"}, 
            status=500
        )

async def get_statistics(request: web_request.Request) -> Response:
    """Получает общую статистику"""
    try:
        stats = get_stats()
        
        logger.info(f"Statistics requested: {stats}")
        
        return web.json_response(stats)
        
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return web.json_response(
            {"error": "Internal server error"}, 
            status=500
        )

def setup_routes(app: web.Application):
    """Настраивает маршруты для API"""
    app.router.add_get('/api/health', health_check)
    app.router.add_get('/api/feed', get_video_feed)
    app.router.add_post('/api/react', send_reaction)
    app.router.add_get('/api/video/{file_id}', get_video_info)
    app.router.add_get('/api/stats', get_statistics)
    
    logger.info("API routes configured")

def create_api_app() -> web.Application:
    """Создает и настраивает API приложение"""
    app = web.Application()
    
    # Настройка CORS
    async def cors_handler(app, handler):
        async def middleware_handler(request):
            if request.method == 'OPTIONS':
                # Preflight запрос
                response = web.Response()
            else:
                response = await handler(request)
            
            # Добавляем CORS заголовки
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Max-Age'] = '86400'
            
            return response
        return middleware_handler
    
    # Добавляем CORS middleware
    app.middlewares.append(cors_handler)
    
    # Настраиваем маршруты
    setup_routes(app)
    
    return app 