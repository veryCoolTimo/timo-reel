import json
import logging
from aiohttp import web
from aiohttp.web_response import Response
from typing import Dict, Any
from utils.cache import (
    get_videos_for_chat, 
    add_reaction, 
    is_user_muted,
    load_metadata
)

logger = logging.getLogger(__name__)

async def get_feed(request: web.Request) -> Response:
    """API endpoint для получения ленты видео для чата"""
    try:
        # Получаем chat_id из параметров запроса
        chat_id = request.query.get('chat_id')
        if not chat_id:
            return web.json_response(
                {'error': 'chat_id parameter is required'}, 
                status=400
            )
        
        try:
            chat_id = int(chat_id)
        except ValueError:
            return web.json_response(
                {'error': 'chat_id must be a valid integer'}, 
                status=400
            )
        
        # Получаем видео для чата
        videos = get_videos_for_chat(chat_id)
        
        # Формируем ответ
        response_data = {
            'success': True,
            'chat_id': chat_id,
            'videos': videos,
            'total': len(videos)
        }
        
        logger.info(f"Feed requested for chat {chat_id}: {len(videos)} videos")
        
        return web.json_response(response_data)
        
    except Exception as e:
        logger.error(f"Error in get_feed: {e}")
        return web.json_response(
            {'error': 'Internal server error'}, 
            status=500
        )

async def send_reaction(request: web.Request) -> Response:
    """API endpoint для отправки реакции (лайк/комментарий)"""
    try:
        # Получаем данные из POST запроса
        data = await request.json()
        
        # Проверяем обязательные поля
        required_fields = ['user_id', 'file_id', 'type']
        for field in required_fields:
            if field not in data:
                return web.json_response(
                    {'error': f'Field {field} is required'}, 
                    status=400
                )
        
        user_id = data['user_id']
        file_id = data['file_id']
        reaction_type = data['type']
        
        # Проверяем тип реакции
        if reaction_type not in ['like', 'comment']:
            return web.json_response(
                {'error': 'Reaction type must be "like" or "comment"'}, 
                status=400
            )
        
        # Проверяем, что user_id - число
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return web.json_response(
                {'error': 'user_id must be a valid integer'}, 
                status=400
            )
        
        # Добавляем реакцию
        add_reaction(user_id, file_id, reaction_type)
        
        # Формируем ответ
        response_data = {
            'success': True,
            'message': f'Reaction {reaction_type} added successfully',
            'user_id': user_id,
            'file_id': file_id,
            'type': reaction_type
        }
        
        logger.info(f"Reaction added: user {user_id}, file {file_id}, type {reaction_type}")
        
        # TODO: В следующем этапе здесь будет отправка уведомления автору видео
        
        return web.json_response(response_data)
        
    except json.JSONDecodeError:
        return web.json_response(
            {'error': 'Invalid JSON in request body'}, 
            status=400
        )
    except Exception as e:
        logger.error(f"Error in send_reaction: {e}")
        return web.json_response(
            {'error': 'Internal server error'}, 
            status=500
        )

async def get_video_info(request: web.Request) -> Response:
    """API endpoint для получения информации о конкретном видео"""
    try:
        file_id = request.match_info.get('file_id')
        if not file_id:
            return web.json_response(
                {'error': 'file_id parameter is required'}, 
                status=400
            )
        
        # Загружаем метаданные
        metadata = load_metadata()
        videos = metadata.get('videos', {})
        
        # Ищем видео
        video_info = videos.get(file_id)
        if not video_info:
            return web.json_response(
                {'error': 'Video not found'}, 
                status=404
            )
        
        # Добавляем file_id к информации
        video_info['file_id'] = file_id
        
        response_data = {
            'success': True,
            'video': video_info
        }
        
        return web.json_response(response_data)
        
    except Exception as e:
        logger.error(f"Error in get_video_info: {e}")
        return web.json_response(
            {'error': 'Internal server error'}, 
            status=500
        )

async def get_stats(request: web.Request) -> Response:
    """API endpoint для получения общей статистики"""
    try:
        metadata = load_metadata()
        
        # Считаем статистику
        total_videos = len(metadata.get('videos', {}))
        total_reactions = sum(
            len(reactions) 
            for reactions in metadata.get('reactions', {}).values()
        )
        total_users = len(metadata.get('user_settings', {}))
        
        # Считаем реакции по типам
        likes_count = 0
        comments_count = 0
        
        for user_reactions in metadata.get('reactions', {}).values():
            for reaction in user_reactions:
                if reaction.get('type') == 'like':
                    likes_count += 1
                elif reaction.get('type') == 'comment':
                    comments_count += 1
        
        response_data = {
            'success': True,
            'stats': {
                'total_videos': total_videos,
                'total_reactions': total_reactions,
                'total_users': total_users,
                'likes_count': likes_count,
                'comments_count': comments_count
            }
        }
        
        return web.json_response(response_data)
        
    except Exception as e:
        logger.error(f"Error in get_stats: {e}")
        return web.json_response(
            {'error': 'Internal server error'}, 
            status=500
        )

async def health_check(request: web.Request) -> Response:
    """Health check endpoint"""
    return web.json_response({
        'status': 'healthy',
        'service': 'TimoReel API',
        'version': '1.0.0'
    })

@web.middleware
async def cors_middleware(request, handler):
    """CORS middleware для разработки"""
    # Обрабатываем preflight OPTIONS запросы
    if request.method == 'OPTIONS':
        response = web.Response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Max-Age'] = '86400'
        return response
    
    # Обрабатываем обычные запросы
    response = await handler(request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

def setup_routes(app: web.Application):
    """Настраивает маршруты для веб-приложения"""
    # API endpoints
    app.router.add_get('/api/feed', get_feed)
    app.router.add_post('/api/react', send_reaction)
    app.router.add_get('/api/video/{file_id}', get_video_info)
    app.router.add_get('/api/stats', get_stats)
    app.router.add_get('/api/health', health_check)
    
    # Добавляем OPTIONS для всех маршрутов
    app.router.add_options('/api/feed', lambda r: web.Response())
    app.router.add_options('/api/react', lambda r: web.Response())
    app.router.add_options('/api/video/{file_id}', lambda r: web.Response())
    app.router.add_options('/api/stats', lambda r: web.Response())
    app.router.add_options('/api/health', lambda r: web.Response())
    
    # Добавляем CORS middleware
    app.middlewares.append(cors_middleware)
    
    logger.info("API routes configured")

async def create_webapp() -> web.Application:
    """Создает веб-приложение для API"""
    app = web.Application()
    setup_routes(app)
    return app 