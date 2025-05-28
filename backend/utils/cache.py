import json
import os
from datetime import datetime
from typing import Dict, List, Any
from .config import METADATA_FILE, STORAGE_PATH, MAX_METADATA_ENTRIES

def ensure_storage_dir():
    """Создает директорию storage если она не существует"""
    os.makedirs(STORAGE_PATH, exist_ok=True)

def load_metadata() -> Dict[str, Any]:
    """Загружает метаданные из JSON файла"""
    ensure_storage_dir()
    
    if not os.path.exists(METADATA_FILE):
        return {"videos": {}, "reactions": {}, "user_settings": {}}
    
    try:
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"videos": {}, "reactions": {}, "user_settings": {}}

def save_metadata(data: Dict[str, Any]):
    """Сохраняет метаданные в JSON файл"""
    ensure_storage_dir()
    
    # Ограничиваем количество записей
    if "videos" in data and len(data["videos"]) > MAX_METADATA_ENTRIES:
        # Сортируем по timestamp и оставляем только последние записи
        sorted_videos = sorted(
            data["videos"].items(),
            key=lambda x: x[1].get("timestamp", 0),
            reverse=True
        )
        data["videos"] = dict(sorted_videos[:MAX_METADATA_ENTRIES])
    
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_video_metadata(file_id: str, chat_id: int, user_id: int, username: str = None):
    """Добавляет метаданные нового видео"""
    data = load_metadata()
    
    data["videos"][file_id] = {
        "chat_id": chat_id,
        "user_id": user_id,
        "username": username,
        "timestamp": datetime.now().isoformat()
    }
    
    save_metadata(data)

def get_videos_for_chat(chat_id: int) -> List[Dict[str, Any]]:
    """Получает все видео для определенного чата"""
    data = load_metadata()
    videos = []
    
    for file_id, metadata in data["videos"].items():
        if metadata["chat_id"] == chat_id:
            videos.append({
                "file_id": file_id,
                **metadata
            })
    
    # Сортируем по времени (новые сначала)
    videos.sort(key=lambda x: x["timestamp"], reverse=True)
    return videos

def add_reaction(user_id: int, file_id: str, reaction_type: str):
    """Добавляет реакцию пользователя"""
    data = load_metadata()
    
    if "reactions" not in data:
        data["reactions"] = {}
    
    if str(user_id) not in data["reactions"]:
        data["reactions"][str(user_id)] = []
    
    reaction = {
        "file_id": file_id,
        "type": reaction_type,
        "timestamp": datetime.now().isoformat()
    }
    
    data["reactions"][str(user_id)].append(reaction)
    save_metadata(data)

def get_user_reactions(user_id: int) -> List[Dict[str, Any]]:
    """Получает все реакции пользователя"""
    data = load_metadata()
    return data.get("reactions", {}).get(str(user_id), [])

def set_user_mute_status(user_id: int, is_muted: bool):
    """Устанавливает статус mute для пользователя"""
    data = load_metadata()
    
    if "user_settings" not in data:
        data["user_settings"] = {}
    
    data["user_settings"][str(user_id)] = {
        "muted": is_muted,
        "updated": datetime.now().isoformat()
    }
    
    save_metadata(data)

def is_user_muted(user_id: int) -> bool:
    """Проверяет, заглушен ли пользователь"""
    data = load_metadata()
    user_settings = data.get("user_settings", {}).get(str(user_id), {})
    return user_settings.get("muted", False) 