#!/usr/bin/env python3
"""
Тест Instagram для серверов с постепенным увеличением агрессивности
"""

import logging
import sys
import time
import random
from downloader.instagram_fix import (
    get_server_specific_config,
    get_fallback_options,
    add_delay_between_requests,
    log_instagram_error
)
import yt_dlp

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_with_config(url: str, config: dict, config_name: str) -> bool:
    """Тестирует URL с конкретной конфигурацией"""
    logger.info(f"🔄 Testing {config_name}...")
    
    try:
        with yt_dlp.YoutubeDL(config) as ydl:
            logger.info(f"  User-Agent: {config.get('http_headers', {}).get('User-Agent', 'Unknown')[:80]}...")
            logger.info(f"  Timeout: {config.get('socket_timeout', 'default')}s")
            logger.info(f"  Retries: {config.get('retries', 'default')}")
            logger.info(f"  Sleep interval: {config.get('sleep_interval', 'default')}")
            
            # Добавляем задержку перед запросом
            delay = config.get('sleep_interval', random.uniform(5, 10))
            if isinstance(delay, (int, float)):
                wait_time = delay
            else:
                wait_time = random.uniform(5, 10)
            
            logger.info(f"  Waiting {wait_time:.1f} seconds before request...")
            time.sleep(wait_time)
            
            info = ydl.extract_info(url, download=False)
            if info:
                logger.info(f"✅ {config_name} SUCCESS!")
                logger.info(f"  Title: {info.get('title', 'Unknown')}")
                logger.info(f"  Uploader: {info.get('uploader', 'Unknown')}")
                logger.info(f"  Duration: {info.get('duration', 0)} seconds")
                return True
            else:
                logger.warning(f"⚠️ {config_name} returned empty info")
                return False
                
    except Exception as e:
        error_msg = str(e)
        logger.error(f"❌ {config_name} FAILED: {error_msg}")
        log_instagram_error(url, f"{config_name}: {error_msg}")
        return False

def test_progressive_instagram(url: str) -> bool:
    """Тестирует Instagram с постепенно более агрессивными настройками"""
    logger.info(f"🎯 Testing Instagram URL: {url}")
    logger.info("📊 Using progressive configuration approach...")
    
    # 1. Начинаем с серверной конфигурации
    logger.info("\n=== Phase 1: Server-specific configuration ===")
    server_config = get_server_specific_config()
    server_config.update({
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    })
    
    if test_with_config(url, server_config, "Server Config"):
        return True
    
    # 2. Пробуем fallback конфигурации
    logger.info("\n=== Phase 2: Fallback configurations ===")
    fallback_configs = get_fallback_options()
    
    for i, config in enumerate(fallback_configs, 1):
        config.update({
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        })
        
        if test_with_config(url, config, f"Fallback Config {i}"):
            return True
        
        # Дополнительная задержка между fallback попытками
        if i < len(fallback_configs):
            wait_time = random.uniform(30, 60)
            logger.info(f"⏳ Waiting {wait_time:.1f} seconds before next attempt...")
            time.sleep(wait_time)
    
    # 3. Последняя попытка с максимальными задержками
    logger.info("\n=== Phase 3: Maximum stealth mode ===")
    stealth_config = get_server_specific_config()
    stealth_config.update({
        'socket_timeout': 300,
        'retries': 50,
        'sleep_interval': random.uniform(60, 120),
        'max_sleep_interval': 180,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'prefer_insecure': True,
        'no_check_certificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
        }
    })
    
    if test_with_config(url, stealth_config, "Maximum Stealth"):
        return True
    
    logger.error("❌ All configuration attempts failed")
    return False

def main():
    """Основная функция тестирования для серверов"""
    logger.info("Instagram Server Test Tool")
    logger.info("=" * 50)
    
    # Тестовые URL (попробуем несколько разных)
    test_urls = [
        "https://www.instagram.com/p/CwxYzNvgzaB/",
        "https://www.instagram.com/reel/C8J2K3LgzaB/",  # Другой пример
    ]
    
    success_count = 0
    total_tests = len(test_urls)
    
    for i, url in enumerate(test_urls, 1):
        logger.info(f"\n{'='*20} TEST {i}/{total_tests} {'='*20}")
        
        if test_progressive_instagram(url):
            success_count += 1
            logger.info(f"✅ Test {i} PASSED - Instagram working!")
            break  # Если один URL работает, этого достаточно
        else:
            logger.error(f"❌ Test {i} FAILED")
            
            if i < total_tests:
                wait_time = random.uniform(120, 180)  # 2-3 минуты между разными URL
                logger.info(f"⏳ Waiting {wait_time:.1f} seconds before next URL...")
                time.sleep(wait_time)
    
    # Результаты
    logger.info("\n" + "=" * 50)
    logger.info(f"Server Test Results: {success_count}/{total_tests} successful")
    
    if success_count > 0:
        logger.info("✅ Instagram integration working on server!")
        logger.info("🎉 Your bot should now be able to download Instagram videos")
        logger.info("\nNext steps:")
        logger.info("1. Restart your bot: python run_background.py restart")
        logger.info("2. Test with real Instagram URL in Telegram")
        logger.info("3. Monitor logs: tail -f logs/bot.log")
    else:
        logger.error("❌ Instagram still not working on server")
        logger.info("\nRecommendations:")
        logger.info("1. 🌐 Consider using proxy servers")
        logger.info("2. 🔄 Try different server location/provider")
        logger.info("3. ⏰ Wait 1-2 hours and try again")
        logger.info("4. 🛡️ Use VPN on server")
        logger.info("5. 📧 Contact your VPS provider about IP reputation")
    
    return success_count > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 