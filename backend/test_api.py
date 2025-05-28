#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API TimoReel
"""

import asyncio
import aiohttp
import json
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(__file__))

from utils.config import HOST, PORT

# URL API сервера
API_BASE_URL = f"http://{HOST}:{PORT + 1}/api"

async def test_health_check():
    """Тестирует health check endpoint"""
    print("🏥 Тестирование health check...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_BASE_URL}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Health check OK: {data}")
                    return True
                else:
                    print(f"❌ Health check failed: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

async def test_stats_endpoint():
    """Тестирует endpoint статистики"""
    print("\n📊 Тестирование stats endpoint...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_BASE_URL}/stats") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Stats OK:")
                    stats = data.get('stats', {})
                    for key, value in stats.items():
                        print(f"  {key}: {value}")
                    return True
                else:
                    print(f"❌ Stats failed: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Stats error: {e}")
        return False

async def test_feed_endpoint():
    """Тестирует endpoint ленты видео"""
    print("\n📹 Тестирование feed endpoint...")
    
    # Тестируем с разными chat_id
    test_chat_ids = [123456789, -1001234567890, 999999999]
    
    for chat_id in test_chat_ids:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{API_BASE_URL}/feed?chat_id={chat_id}") as response:
                    if response.status == 200:
                        data = await response.json()
                        video_count = data.get('total', 0)
                        print(f"✅ Feed for chat {chat_id}: {video_count} videos")
                    else:
                        print(f"❌ Feed failed for chat {chat_id}: {response.status}")
                        return False
        except Exception as e:
            print(f"❌ Feed error for chat {chat_id}: {e}")
            return False
    
    # Тестируем без chat_id (должно вернуть ошибку)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_BASE_URL}/feed") as response:
                if response.status == 400:
                    print("✅ Feed correctly rejects missing chat_id")
                else:
                    print(f"❌ Feed should reject missing chat_id, got {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Feed error testing missing chat_id: {e}")
        return False
    
    return True

async def test_reaction_endpoint():
    """Тестирует endpoint реакций"""
    print("\n❤️ Тестирование reaction endpoint...")
    
    # Тестовые данные
    test_reactions = [
        {"user_id": 123456789, "file_id": "test_file_1", "type": "like"},
        {"user_id": 987654321, "file_id": "test_file_2", "type": "comment"},
    ]
    
    for reaction in test_reactions:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{API_BASE_URL}/react",
                    json=reaction,
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ Reaction added: {reaction['type']} from user {reaction['user_id']}")
                    else:
                        print(f"❌ Reaction failed: {response.status}")
                        text = await response.text()
                        print(f"   Response: {text}")
                        return False
        except Exception as e:
            print(f"❌ Reaction error: {e}")
            return False
    
    # Тестируем неправильные данные
    invalid_reactions = [
        {},  # Пустой объект
        {"user_id": "invalid", "file_id": "test", "type": "like"},  # Неправильный user_id
        {"user_id": 123, "file_id": "test", "type": "invalid"},  # Неправильный type
    ]
    
    for invalid_reaction in invalid_reactions:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{API_BASE_URL}/react",
                    json=invalid_reaction,
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    if response.status == 400:
                        print(f"✅ Correctly rejected invalid reaction: {invalid_reaction}")
                    else:
                        print(f"❌ Should reject invalid reaction: {invalid_reaction}")
                        return False
        except Exception as e:
            print(f"❌ Error testing invalid reaction: {e}")
            return False
    
    return True

async def test_video_info_endpoint():
    """Тестирует endpoint информации о видео"""
    print("\n🎬 Тестирование video info endpoint...")
    
    # Тестируем с несуществующим file_id
    test_file_id = "nonexistent_file_id"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_BASE_URL}/video/{test_file_id}") as response:
                if response.status == 404:
                    print(f"✅ Correctly returned 404 for nonexistent video")
                    return True
                else:
                    print(f"❌ Should return 404 for nonexistent video, got {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Video info error: {e}")
        return False

async def main():
    """Основная функция тестирования API"""
    print("🚀 Запуск тестов TimoReel API\n")
    print(f"API URL: {API_BASE_URL}")
    
    tests = [
        ("Health Check", test_health_check),
        ("Stats Endpoint", test_stats_endpoint),
        ("Feed Endpoint", test_feed_endpoint),
        ("Reaction Endpoint", test_reaction_endpoint),
        ("Video Info Endpoint", test_video_info_endpoint),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if await test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED\n")
            else:
                print(f"❌ {test_name} - FAILED\n")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}\n")
    
    print(f"📊 Результаты: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты API пройдены!")
        return True
    else:
        print("⚠️  Некоторые тесты API не пройдены.")
        print("💡 Убедитесь, что API сервер запущен: python api_server.py")
        return False

if __name__ == '__main__':
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Тестирование прервано пользователем")
        sys.exit(1) 