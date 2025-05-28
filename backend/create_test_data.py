#!/usr/bin/env python3
"""
Скрипт для создания тестовых данных для демонстрации WebApp
"""

import sys
import os
import time

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(__file__))

from utils.cache import add_video_metadata, add_reaction

def create_test_videos():
    """Создает тестовые видео"""
    print("🎬 Создание тестовых видео...")
    
    # Тестовые видео для чата 123456789
    test_videos = [
        {
            "file_id": "test_video_1",
            "chat_id": 123456789,
            "user_id": 111111111,
            "username": "alice_wonder"
        },
        {
            "file_id": "test_video_2", 
            "chat_id": 123456789,
            "user_id": 222222222,
            "username": "bob_creator"
        },
        {
            "file_id": "test_video_3",
            "chat_id": 123456789,
            "user_id": 333333333,
            "username": "charlie_films"
        },
        {
            "file_id": "test_video_4",
            "chat_id": 123456789,
            "user_id": 444444444,
            "username": "diana_dance"
        },
        {
            "file_id": "test_video_5",
            "chat_id": 123456789,
            "user_id": 555555555,
            "username": "eve_music"
        }
    ]
    
    # Добавляем видео с разными временными метками
    base_time = int(time.time())
    
    for i, video in enumerate(test_videos):
        # Делаем видео с разными временными метками (от новых к старым)
        timestamp_offset = i * 3600  # Каждое видео на час старше предыдущего
        
        # Временно изменяем время для создания истории
        original_time = time.time
        time.time = lambda: base_time - timestamp_offset
        
        add_video_metadata(
            video["file_id"],
            video["chat_id"], 
            video["user_id"],
            video["username"]
        )
        
        # Восстанавливаем время
        time.time = original_time
        
        print(f"✅ Добавлено видео: {video['username']} ({video['file_id']})")

def create_test_reactions():
    """Создает тестовые реакции"""
    print("\n❤️ Создание тестовых реакций...")
    
    # Тестовые реакции
    test_reactions = [
        {"user_id": 123456789, "file_id": "test_video_1", "type": "like"},
        {"user_id": 123456789, "file_id": "test_video_2", "type": "comment"},
        {"user_id": 123456789, "file_id": "test_video_3", "type": "like"},
        {"user_id": 987654321, "file_id": "test_video_1", "type": "like"},
        {"user_id": 987654321, "file_id": "test_video_4", "type": "comment"},
        {"user_id": 111111111, "file_id": "test_video_2", "type": "like"},
        {"user_id": 222222222, "file_id": "test_video_3", "type": "comment"},
    ]
    
    for reaction in test_reactions:
        add_reaction(
            reaction["user_id"],
            reaction["file_id"], 
            reaction["type"]
        )
        print(f"✅ Добавлена реакция: {reaction['type']} от пользователя {reaction['user_id']}")

def main():
    """Основная функция"""
    print("🚀 Создание тестовых данных для TimoReel WebApp\n")
    
    try:
        create_test_videos()
        create_test_reactions()
        
        print("\n🎉 Тестовые данные созданы успешно!")
        print("\n📋 Что создано:")
        print("• 5 тестовых видео для чата 123456789")
        print("• 7 тестовых реакций от разных пользователей")
        print("• Видео с разными временными метками")
        
        print("\n🌐 Теперь можно:")
        print("1. Запустить API сервер: python api_server.py")
        print("2. Запустить WebApp: cd ../webapp && npm run dev")
        print("3. Открыть http://localhost:3000 в браузере")
        
    except Exception as e:
        print(f"❌ Ошибка создания тестовых данных: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 