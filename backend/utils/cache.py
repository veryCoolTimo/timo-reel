#!/usr/bin/env python3
"""
Система кеширования и работы с метаданными
"""

import json
import os
import time
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

# Путь к файлу метаданных
STORAGE_DIR = os.path.join(os.path.dirname(__file__), '..', 'storage')
METADATA_FILE = os.path.join(STORAGE_DIR, 'metadata.json')

# Ограничения
MAX_VIDEOS = 500
MAX_REACTIONS_PER_USER = 100

def ensure_storage_dir():
    """Создает директорию storage если её нет"""
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
        logger.info(f"Created storage directory: {STORAGE_DIR}")

def load_metadata() -> Dict[str, Any]:
    """Загружает метаданные из JSON файла"""
    ensure_storage_dir()
    
    if not os.path.exists(METADATA_FILE):
        # Создаем пустой файл с базовой структурой
        default_data = {
            "videos": {},
            "reactions": {},
            "user_settings": {},
            "stats": {
                "total_videos": 0,
                "total_reactions": 0,
                "created_at": int(time.time())
            }
        }
        save_metadata(default_data)
        return default_data
    
    try:
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Проверяем структуру и добавляем недостающие поля
        if "user_settings" not in data:
            data["user_settings"] = {}
        if "stats" not in data:
            data["stats"] = {
                "total_videos": len(data.get("videos", {})),
                "total_reactions": sum(len(reactions) for reactions in data.get("reactions", {}).values()),
                "created_at": int(time.time())
            }
            
        return data
        
    except Exception as e:
        logger.error(f"Error loading metadata: {e}")
        # Возвращаем пустую структуру в случае ошибки
        return {
            "videos": {},
            "reactions": {},
            "user_settings": {},
            "stats": {"total_videos": 0, "total_reactions": 0, "created_at": int(time.time())}
        }

def save_metadata(data: Dict[str, Any]):
    """Сохраняет метаданные в JSON файл"""
    ensure_storage_dir()
    
    try:
        # Ограничиваем размер данных
        if "videos" in data and len(data["videos"]) > MAX_VIDEOS:
            # Удаляем старые видео
            videos_items = list(data["videos"].items())
            videos_items.sort(key=lambda x: x[1].get("timestamp", 0))
            data["videos"] = dict(videos_items[-MAX_VIDEOS:])
            logger.info(f"Trimmed videos to {MAX_VIDEOS} entries")
        
        # Ограничиваем реакции на пользователя
        if "reactions" in data:
            for user_id, reactions in data["reactions"].items():
                if len(reactions) > MAX_REACTIONS_PER_USER:
                    reactions.sort(key=lambda x: x.get("timestamp", 0))
                    data["reactions"][user_id] = reactions[-MAX_REACTIONS_PER_USER:]
        
        # Обновляем статистику
        data["stats"] = {
            "total_videos": len(data.get("videos", {})),
            "total_reactions": sum(len(reactions) for reactions in data.get("reactions", {}).values()),
            "last_updated": int(time.time())
        }
        
        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        logger.debug(f"Metadata saved: {len(data.get('videos', {}))} videos, {data['stats']['total_reactions']} reactions")
        
    except Exception as e:
        logger.error(f"Error saving metadata: {e}")

def add_video_metadata(file_id: str, chat_id: int, user_id: int, username: str):
    """Добавляет метаданные нового видео"""
    data = load_metadata()
    
    data["videos"][file_id] = {
        "chat_id": chat_id,
        "user_id": user_id,
        "username": username,
        "timestamp": int(time.time())
    }
    
    save_metadata(data)
    logger.info(f"Added video metadata: {file_id} from user {user_id}")

def get_videos_for_chat(chat_id: int) -> List[Dict[str, Any]]:
    """Получает все видео для указанного чата"""
    data = load_metadata()
    videos = []
    
    for file_id, video_info in data["videos"].items():
        if video_info["chat_id"] == chat_id:
            videos.append({
                "file_id": file_id,
                "user_id": video_info["user_id"],
                "username": video_info["username"],
                "timestamp": video_info["timestamp"]
            })
    
    # Сортируем по времени (новые сначала)
    videos.sort(key=lambda x: x["timestamp"], reverse=True)
    
    logger.debug(f"Found {len(videos)} videos for chat {chat_id}")
    return videos

def add_reaction(user_id: int, file_id: str, reaction_type: str):
    """Добавляет реакцию пользователя"""
    data = load_metadata()
    
    if "reactions" not in data:
        data["reactions"] = {}
    
    user_id_str = str(user_id)
    if user_id_str not in data["reactions"]:
        data["reactions"][user_id_str] = []
    
    # Добавляем новую реакцию
    reaction = {
        "file_id": file_id,
        "type": reaction_type,
        "timestamp": int(time.time())
    }
    
    data["reactions"][user_id_str].append(reaction)
    
    save_metadata(data)
    logger.info(f"Added reaction: user {user_id} {reaction_type} video {file_id}")

def get_video_author(file_id: str) -> dict:
    """Получает информацию об авторе видео"""
    metadata = load_metadata()
    videos = metadata.get('videos', {})
    
    video_info = videos.get(file_id)
    if not video_info:
        return None
    
    return {
        'user_id': video_info.get('user_id'),
        'username': video_info.get('username')
    }

def get_user_reactions(user_id: int) -> List[Dict[str, Any]]:
    """Получает все реакции пользователя"""
    data = load_metadata()
    user_id_str = str(user_id)
    
    return data.get("reactions", {}).get(user_id_str, [])

def get_user_settings(user_id: int) -> dict:
    """Получает настройки пользователя"""
    metadata = load_metadata()
    user_settings = metadata.get('user_settings', {})
    return user_settings.get(str(user_id), {})

def update_user_settings(user_id: int, settings: dict):
    """Обновляет настройки пользователя"""
    metadata = load_metadata()
    
    if 'user_settings' not in metadata:
        metadata['user_settings'] = {}
    
    user_key = str(user_id)
    if user_key not in metadata['user_settings']:
        metadata['user_settings'][user_key] = {}
    
    # Обновляем настройки
    metadata['user_settings'][user_key].update(settings)
    
    save_metadata(metadata)
    logger.info(f"Updated settings for user {user_id}: {settings}")

def is_user_muted(user_id: int) -> bool:
    """Проверяет, отключены ли уведомления у пользователя"""
    settings = get_user_settings(user_id)
    return settings.get('muted', False)

def set_user_mute_status(user_id: int, muted: bool):
    """Устанавливает статус уведомлений для пользователя"""
    settings = {'muted': muted}
    update_user_settings(user_id, settings)
    logger.info(f"Set mute status for user {user_id}: {muted}")

def get_stats() -> dict:
    """Получает общую статистику системы"""
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
    
    return {
        'total_videos': total_videos,
        'total_reactions': total_reactions,
        'total_users': total_users,
        'likes_count': likes_count,
        'comments_count': comments_count
    } 