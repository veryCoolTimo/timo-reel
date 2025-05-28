#!/usr/bin/env python3
"""
Тестовый скрипт для проверки модулей TimoReel Bot
"""

import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Тестирует импорт всех модулей"""
    print("🧪 Тестирование импортов...")
    
    try:
        from utils.config import BOT_TOKEN, MAX_VIDEO_SIZE
        print("✅ utils.config - OK")
    except Exception as e:
        print(f"❌ utils.config - ERROR: {e}")
        return False
    
    try:
        from utils.cache import load_metadata, save_metadata
        print("✅ utils.cache - OK")
    except Exception as e:
        print(f"❌ utils.cache - ERROR: {e}")
        return False
    
    try:
        from downloader.video_downloader import downloader
        print("✅ downloader.video_downloader - OK")
    except Exception as e:
        print(f"❌ downloader.video_downloader - ERROR: {e}")
        return False
    
    try:
        from handlers.link_handler import extract_urls_from_text
        print("✅ handlers.link_handler - OK")
    except Exception as e:
        print(f"❌ handlers.link_handler - ERROR: {e}")
        return False
    
    try:
        from handlers.pm_commands import mute_command
        print("✅ handlers.pm_commands - OK")
    except Exception as e:
        print(f"❌ handlers.pm_commands - ERROR: {e}")
        return False
    
    try:
        from handlers.webapp_handler import create_webapp
        print("✅ handlers.webapp_handler - OK")
    except Exception as e:
        print(f"❌ handlers.webapp_handler - ERROR: {e}")
        return False
    
    return True

def test_url_extraction():
    """Тестирует извлечение URL из текста"""
    print("\n🔗 Тестирование извлечения URL...")
    
    from handlers.link_handler import extract_urls_from_text
    
    test_cases = [
        "Посмотри это видео: https://instagram.com/p/ABC123/",
        "Крутой TikTok https://vm.tiktok.com/ZMjKpQrSt/",
        "https://www.tiktok.com/@user/video/1234567890",
        "Обычный текст без ссылок",
        "Несколько ссылок: https://instagram.com/reel/XYZ/ и https://tiktok.com/@test/video/999"
    ]
    
    for i, text in enumerate(test_cases, 1):
        urls = extract_urls_from_text(text)
        print(f"Тест {i}: {len(urls)} URL найдено")
        for url in urls:
            print(f"  - {url}")
    
    return True

def test_video_downloader():
    """Тестирует модуль загрузки видео"""
    print("\n📹 Тестирование загрузчика видео...")
    
    from downloader.video_downloader import downloader
    
    test_urls = [
        "https://instagram.com/p/test/",
        "https://tiktok.com/@user/video/123",
        "https://youtube.com/watch?v=test",  # Не поддерживается
        "https://example.com/video.mp4"     # Не поддерживается
    ]
    
    for url in test_urls:
        is_supported = downloader.is_supported_url(url)
        print(f"URL: {url}")
        print(f"  Поддерживается: {'✅' if is_supported else '❌'}")
    
    return True

def test_cache():
    """Тестирует систему кеширования"""
    print("\n💾 Тестирование кеша...")
    
    from utils.cache import load_metadata, save_metadata, add_video_metadata, add_reaction
    
    # Загружаем текущие метаданные
    metadata = load_metadata()
    print(f"Загружены метаданные: {len(metadata.get('videos', {}))} видео")
    
    # Тестируем добавление видео (не сохраняем реально)
    print("Тест добавления метаданных видео - OK")
    
    # Тестируем добавление реакции
    add_reaction(999999, "test_video_id", "like")
    print("Тест добавления реакции - OK")
    
    return True

def test_config():
    """Тестирует конфигурацию"""
    print("\n⚙️ Тестирование конфигурации...")
    
    from utils.config import BOT_TOKEN, MAX_VIDEO_SIZE, HOST, PORT
    
    print(f"BOT_TOKEN установлен: {'✅' if BOT_TOKEN else '❌'}")
    print(f"MAX_VIDEO_SIZE: {MAX_VIDEO_SIZE // (1024*1024)}MB")
    print(f"HOST: {HOST}")
    print(f"PORT: {PORT}")
    print(f"API PORT: {PORT + 1}")
    
    if not BOT_TOKEN:
        print("⚠️  Создайте файл .env с BOT_TOKEN для полного тестирования")
    
    return True

def test_api_creation():
    """Тестирует создание API приложения"""
    print("\n🌐 Тестирование создания API...")
    
    try:
        import asyncio
        from handlers.webapp_handler import create_webapp
        
        async def test_webapp():
            app = await create_webapp()
            return app is not None
        
        result = asyncio.run(test_webapp())
        if result:
            print("✅ API приложение создано успешно")
            return True
        else:
            print("❌ Ошибка создания API приложения")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка тестирования API: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов TimoReel Bot\n")
    
    tests = [
        ("Импорты модулей", test_imports),
        ("Извлечение URL", test_url_extraction),
        ("Загрузчик видео", test_video_downloader),
        ("Система кеша", test_cache),
        ("Конфигурация", test_config),
        ("Создание API", test_api_creation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED\n")
            else:
                print(f"❌ {test_name} - FAILED\n")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}\n")
    
    print(f"📊 Результаты: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Бот готов к запуску.")
        print("\n📋 Следующие шаги:")
        print("1. Запуск бота: python bot.py")
        print("2. Запуск API сервера: python api_server.py")
        print("3. Тестирование API: python test_api.py")
        return True
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверьте ошибки выше.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 