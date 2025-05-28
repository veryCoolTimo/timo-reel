#!/usr/bin/env python3
"""
Диагностический скрипт для тестирования загрузки из Instagram
"""

import sys
import os
import logging
from downloader.video_downloader import VideoDownloader
import yt_dlp

# Настройка подробного логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_yt_dlp_direct(url):
    """Тестирует прямую загрузку через yt-dlp"""
    print(f"\n🔍 Тестирование прямой загрузки yt-dlp для: {url}")
    
    opts = {
        'quiet': False,
        'verbose': True,
        'extract_flat': False,
        'no_warnings': False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"✅ Extraction successful!")
            print(f"   Title: {info.get('title', 'N/A')}")
            print(f"   Duration: {info.get('duration', 'N/A')} seconds")
            print(f"   Uploader: {info.get('uploader', 'N/A')}")
            print(f"   Filesize: {info.get('filesize', 'N/A')} bytes")
            print(f"   Format: {info.get('ext', 'N/A')}")
            return True
    except Exception as e:
        print(f"❌ Direct yt-dlp failed: {e}")
        return False

def test_video_downloader(url):
    """Тестирует наш VideoDownloader"""
    print(f"\n🔍 Тестирование VideoDownloader для: {url}")
    
    downloader = VideoDownloader()
    
    # Проверка поддержки URL
    if not downloader.is_supported_url(url):
        print(f"❌ URL не поддерживается: {url}")
        return False
    
    print("✅ URL поддерживается")
    
    # Извлечение информации
    print("📋 Извлечение информации...")
    info = downloader.extract_info(url)
    if info:
        print(f"✅ Информация получена:")
        for key, value in info.items():
            print(f"   {key}: {value}")
    else:
        print("❌ Не удалось получить информацию о видео")
        return False
    
    # Загрузка видео
    print("⬇️ Загрузка видео...")
    try:
        file_path = downloader.download_video(url)
        if file_path:
            file_size = os.path.getsize(file_path)
            print(f"✅ Видео загружено: {file_path}")
            print(f"   Размер файла: {file_size} bytes")
            
            # Очистка
            downloader.cleanup_file(file_path)
            print("🧹 Временный файл удален")
            return True
        else:
            print("❌ Загрузка не удалась")
            return False
    except Exception as e:
        print(f"❌ Ошибка при загрузке: {e}")
        return False

def print_system_info():
    """Выводит информацию о системе"""
    print("🖥️ Информация о системе:")
    print(f"   Python: {sys.version}")
    print(f"   OS: {os.name}")
    print(f"   Current directory: {os.getcwd()}")
    
    try:
        import yt_dlp
        print(f"   yt-dlp version: {yt_dlp.version.__version__}")
    except:
        print("   yt-dlp version: не удалось определить")

def main():
    print("🧪 TimoReel Instagram Download Diagnostic")
    print("=" * 50)
    
    print_system_info()
    
    # Тестовые URL (замените на актуальные)
    test_urls = [
        "https://www.instagram.com/reel/test",  # Замените на реальный URL
        # Добавьте больше URL для тестирования
    ]
    
    if len(sys.argv) > 1:
        test_urls = [sys.argv[1]]
        print(f"\n🎯 Тестирование пользовательского URL: {sys.argv[1]}")
    else:
        print("\n💡 Использование: python test_instagram_download.py <instagram_url>")
        print("💡 Или запустите без аргументов для тестирования встроенных URL")
        return
    
    for url in test_urls:
        if not url or url == "https://www.instagram.com/reel/test":
            print(f"\n⚠️ Пропускаем тестовый URL: {url}")
            continue
            
        print(f"\n" + "=" * 80)
        print(f"🧪 ТЕСТИРОВАНИЕ: {url}")
        print("=" * 80)
        
        # Тест 1: Прямой yt-dlp
        success1 = test_yt_dlp_direct(url)
        
        # Тест 2: Наш VideoDownloader
        success2 = test_video_downloader(url)
        
        print(f"\n📊 Результаты для {url}:")
        print(f"   Прямой yt-dlp: {'✅ SUCCESS' if success1 else '❌ FAILED'}")
        print(f"   VideoDownloader: {'✅ SUCCESS' if success2 else '❌ FAILED'}")

if __name__ == "__main__":
    main() 