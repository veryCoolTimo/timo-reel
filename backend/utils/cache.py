import json
import os
import time
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Путь к файлу метаданных
METADATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'storage', 'metadata.json')

# Максимальное количество записей (для ограничения размера файла)
MAX_VIDEOS = 500
MAX_REACTIONS_PER_USER = 100

def ensure_storage_dir():
    """Создает директорию storage если её нет"""
    storage_dir = os.path.dirname(METADATA_FILE)
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)

def load_metadata() -> Dict[str, Any]:
    """Загружает метаданные из JSON файла"""
    ensure_storage_dir()
    
    if not os.path.exists(METADATA_FILE):
        # Создаем пустой файл с базовой структурой
        default_data = {
            "videos": {},
            "reactions": {},
            "user_settings": {}
        }
        save_metadata(default_data)
        return default_data
    
    try:
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading metadata: {e}")
        return {"videos": {}, "reactions": {}, "user_settings": {}}

def save_metadata(data: Dict[str, Any]):
    """Сохраняет метаданные в JSON файл"""
    ensure_storage_dir()
    
    try:
        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving metadata: {e}")

def add_video_metadata(file_id: str, chat_id: int, user_id: int, username: str):
    """Добавляет метаданные нового видео"""
    metadata = load_metadata()
    
    # Добавляем информацию о видео
    metadata["videos"][file_id] = {
        "chat_id": chat_id,
        "user_id": user_id,
        "username": username,
        "timestamp": int(time.time())
    }
    
    # Ограничиваем количество видео
    videos = metadata["videos"]
    if len(videos) > MAX_VIDEOS:
        # Удаляем самые старые видео
        sorted_videos = sorted(
            videos.items(), 
            key=lambda x: x[1].get("timestamp", 0)
        )
        
        # Оставляем только последние MAX_VIDEOS
        videos_to_keep = dict(sorted_videos[-MAX_VIDEOS:])
        metadata["videos"] = videos_to_keep
        
        logger.info(f"Trimmed videos to {MAX_VIDEOS} entries")
    
    save_metadata(metadata)
    logger.info(f"Added video metadata: {file_id}")

def get_videos_for_chat(chat_id: int) -> List[Dict[str, Any]]:
    """Получает все видео для указанного чата"""
    metadata = load_metadata()
    videos = metadata.get("videos", {})
    
    # Фильтруем видео по chat_id
    chat_videos = []
    for file_id, video_info in videos.items():
        if video_info.get("chat_id") == chat_id:
            video_data = video_info.copy()
            video_data["file_id"] = file_id
            chat_videos.append(video_data)
    
    # Сортируем по времени (новые сначала)
    chat_videos.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
    
    return chat_videos

def add_reaction(user_id: int, file_id: str, reaction_type: str):
    """Добавляет реакцию пользователя"""
    metadata = load_metadata()
    
    # Инициализируем структуру реакций если нужно
    if "reactions" not in metadata:
        metadata["reactions"] = {}
    
    user_id_str = str(user_id)
    if user_id_str not in metadata["reactions"]:
        metadata["reactions"][user_id_str] = []
    
    # Добавляем новую реакцию
    reaction = {
        "file_id": file_id,
        "type": reaction_type,
        "timestamp": int(time.time())
    }
    
    metadata["reactions"][user_id_str].append(reaction)
    
    # Ограничиваем количество реакций на пользователя
    user_reactions = metadata["reactions"][user_id_str]
    if len(user_reactions) > MAX_REACTIONS_PER_USER:
        # Оставляем только последние реакции
        metadata["reactions"][user_id_str] = user_reactions[-MAX_REACTIONS_PER_USER:]
        logger.info(f"Trimmed reactions for user {user_id} to {MAX_REACTIONS_PER_USER}")
    
    save_metadata(metadata)
    logger.info(f"Added reaction: user {user_id}, file {file_id}, type {reaction_type}")

def get_user_reactions(user_id: int) -> List[Dict[str, Any]]:
    """Получает все реакции пользователя"""
    metadata = load_metadata()
    reactions = metadata.get("reactions", {})
    
    user_id_str = str(user_id)
    return reactions.get(user_id_str, [])

def set_user_mute_status(user_id: int, is_muted: bool):
    """Устанавливает статус уведомлений для пользователя"""
    metadata = load_metadata()
    
    if "user_settings" not in metadata:
        metadata["user_settings"] = {}
    
    user_id_str = str(user_id)
    if user_id_str not in metadata["user_settings"]:
        metadata["user_settings"][user_id_str] = {}
    
    metadata["user_settings"][user_id_str]["muted"] = is_muted
    metadata["user_settings"][user_id_str]["updated"] = int(time.time())
    
    save_metadata(metadata)
    logger.info(f"User {user_id} mute status set to {is_muted}")

def is_user_muted(user_id: int) -> bool:
    """Проверяет, отключены ли уведомления у пользователя"""
    metadata = load_metadata()
    user_settings = metadata.get("user_settings", {})
    
    user_id_str = str(user_id)
    user_data = user_settings.get(user_id_str, {})
    
    return user_data.get("muted", False)

def get_video_author(file_id: str) -> Optional[Dict[str, Any]]:
    """Получает информацию об авторе видео"""
    metadata = load_metadata()
    videos = metadata.get("videos", {})
    
    video_info = videos.get(file_id)
    if video_info:
        return {
            "user_id": video_info.get("user_id"),
            "username": video_info.get("username"),
            "chat_id": video_info.get("chat_id")
        }
    
    return None 