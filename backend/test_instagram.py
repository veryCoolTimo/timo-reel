#!/usr/bin/env python3
"""
Простой тест Instagram загрузки
"""

import logging
import sys
from downloader.video_downloader import downloader

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_instagram_url(url):
    """Тестирует загрузку Instagram URL"""
    logger.info(f"Testing Instagram URL: {url}")
    
    try:
        # Тестируем извлечение информации
        logger.info("Extracting video info...")
        result = downloader.extract_info(url)
        
        if result:
            logger.info("✅ Success! Video info extracted:")
            logger.info(f"  Title: {result.get('title', 'Unknown')}")
            logger.info(f"  Uploader: {result.get('uploader', 'Unknown')}")
            logger.info(f"  Duration: {result.get('duration', 0)} seconds")
            logger.info(f"  File size: {result.get('filesize', 0)} bytes")
            return True
        else:
            logger.error("❌ Failed to extract video info")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during extraction: {e}")
        return False

def test_download(url):
    """Тестирует полную загрузку видео"""
    logger.info(f"Testing full download for: {url}")
    
    try:
        file_path = downloader.download_video(url)
        
        if file_path:
            logger.info(f"✅ Download successful: {file_path}")
            # Очищаем файл
            downloader.cleanup_file(file_path)
            logger.info("Temporary file cleaned up")
            return True
        else:
            logger.error("❌ Download failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during download: {e}")
        return False

def main():
    """Основная функция тестирования"""
    logger.info("Instagram Download Test")
    logger.info("=" * 40)
    
    # Тестовые URL (публичные посты)
    test_urls = [
        "https://www.instagram.com/p/CwxYzNvgzaB/",  # Пример 1
        "https://www.instagram.com/reel/C123456789/",  # Пример 2 (может не существовать)
    ]
    
    success_count = 0
    total_tests = 0
    
    for url in test_urls:
        total_tests += 1
        logger.info(f"\n--- Test {total_tests}: {url} ---")
        
        # Тест извлечения информации
        if test_instagram_url(url):
            success_count += 1
            
            # Если извлечение успешно, тестируем загрузку
            logger.info("Info extraction successful, testing download...")
            if test_download(url):
                logger.info("✅ Full download test passed")
            else:
                logger.warning("⚠️ Download test failed (but info extraction worked)")
        else:
            logger.error("❌ Info extraction failed, skipping download test")
    
    # Результаты
    logger.info("\n" + "=" * 40)
    logger.info(f"Test Results: {success_count}/{total_tests} successful")
    
    if success_count > 0:
        logger.info("✅ Instagram integration is working!")
        logger.info("The bot should be able to download Instagram videos on the server.")
    else:
        logger.error("❌ Instagram integration is not working")
        logger.info("Recommendations:")
        logger.info("1. Check if cookies are valid")
        logger.info("2. Try different Instagram URLs")
        logger.info("3. Check network connectivity")
        logger.info("4. Run: python instagram_diagnostic.py")
    
    return success_count > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 