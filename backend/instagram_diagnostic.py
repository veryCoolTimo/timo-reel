#!/usr/bin/env python3
"""
Диагностика проблем с Instagram
Помогает выявить причины блокировок и rate-limit
"""

import os
import sys
import logging
import requests
import subprocess
import platform
from datetime import datetime
from typing import Dict, List

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_system_info():
    """Проверяет информацию о системе"""
    logger.info("=== SYSTEM INFORMATION ===")
    
    info = {
        'platform': platform.platform(),
        'system': platform.system(),
        'machine': platform.machine(),
        'python_version': platform.python_version(),
        'hostname': platform.node(),
    }
    
    for key, value in info.items():
        logger.info(f"{key}: {value}")
    
    # Проверяем, запущено ли на сервере
    is_server = os.path.exists('/etc/os-release') or os.path.exists('/proc/version')
    logger.info(f"Server environment: {'Yes' if is_server else 'No'}")
    
    return info

def check_network_connectivity():
    """Проверяет сетевое подключение"""
    logger.info("\n=== NETWORK CONNECTIVITY ===")
    
    test_urls = [
        'https://www.google.com',
        'https://www.instagram.com',
        'https://api.instagram.com',
        'https://www.youtube.com',
    ]
    
    results = {}
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            results[url] = {
                'status': response.status_code,
                'success': True,
                'response_time': response.elapsed.total_seconds()
            }
            logger.info(f"✅ {url}: {response.status_code} ({response.elapsed.total_seconds():.2f}s)")
        except Exception as e:
            results[url] = {
                'status': None,
                'success': False,
                'error': str(e)
            }
            logger.error(f"❌ {url}: {e}")
    
    return results

def check_ip_reputation():
    """Проверяет репутацию IP адреса"""
    logger.info("\n=== IP REPUTATION CHECK ===")
    
    try:
        # Получаем внешний IP
        response = requests.get('https://httpbin.org/ip', timeout=10)
        ip_info = response.json()
        external_ip = ip_info.get('origin', 'Unknown')
        logger.info(f"External IP: {external_ip}")
        
        # Проверяем геолокацию
        try:
            geo_response = requests.get(f'https://ipapi.co/{external_ip}/json/', timeout=10)
            geo_data = geo_response.json()
            logger.info(f"Location: {geo_data.get('city', 'Unknown')}, {geo_data.get('country_name', 'Unknown')}")
            logger.info(f"ISP: {geo_data.get('org', 'Unknown')}")
            
            # Проверяем, является ли IP серверным/VPS
            org = geo_data.get('org', '').lower()
            server_indicators = ['amazon', 'google', 'microsoft', 'digitalocean', 'linode', 'vultr', 'hetzner']
            is_server_ip = any(indicator in org for indicator in server_indicators)
            logger.info(f"Server/VPS IP: {'Yes' if is_server_ip else 'No'}")
            
            if is_server_ip:
                logger.warning("⚠️ Server IPs are more likely to be blocked by Instagram")
            
        except Exception as e:
            logger.error(f"Geo lookup failed: {e}")
        
        return external_ip
        
    except Exception as e:
        logger.error(f"IP check failed: {e}")
        return None

def check_yt_dlp_version():
    """Проверяет версию yt-dlp"""
    logger.info("\n=== YT-DLP VERSION CHECK ===")
    
    try:
        import yt_dlp
        version = yt_dlp.version.__version__
        logger.info(f"yt-dlp version: {version}")
        
        # Проверяем, актуальная ли версия
        try:
            response = requests.get('https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest', timeout=10)
            latest_release = response.json()
            latest_version = latest_release['tag_name']
            logger.info(f"Latest version: {latest_version}")
            
            if version != latest_version:
                logger.warning(f"⚠️ yt-dlp is outdated. Consider updating: pip install -U yt-dlp")
            else:
                logger.info("✅ yt-dlp is up to date")
                
        except Exception as e:
            logger.error(f"Version check failed: {e}")
        
        return version
        
    except ImportError:
        logger.error("❌ yt-dlp not installed")
        return None

def test_instagram_access():
    """Тестирует доступ к Instagram"""
    logger.info("\n=== INSTAGRAM ACCESS TEST ===")
    
    test_urls = [
        'https://www.instagram.com',
        'https://www.instagram.com/robots.txt',
        'https://i.instagram.com',
    ]
    
    results = {}
    
    for url in test_urls:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            results[url] = {
                'status': response.status_code,
                'success': response.status_code == 200,
                'headers': dict(response.headers),
                'content_length': len(response.content)
            }
            
            if response.status_code == 200:
                logger.info(f"✅ {url}: {response.status_code}")
            elif response.status_code == 429:
                logger.error(f"❌ {url}: Rate limited (429)")
            elif response.status_code == 403:
                logger.error(f"❌ {url}: Forbidden (403) - IP may be blocked")
            else:
                logger.warning(f"⚠️ {url}: {response.status_code}")
                
        except Exception as e:
            results[url] = {
                'status': None,
                'success': False,
                'error': str(e)
            }
            logger.error(f"❌ {url}: {e}")
    
    return results

def test_yt_dlp_instagram():
    """Тестирует yt-dlp с Instagram"""
    logger.info("\n=== YT-DLP INSTAGRAM TEST ===")
    
    # Тестовая ссылка (публичное видео)
    test_url = "https://www.instagram.com/p/CwxYzNvgzaB/"  # Пример публичного поста
    
    try:
        import yt_dlp
        
        # Базовые настройки
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'format': 'best',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        }
        
        logger.info(f"Testing URL: {test_url}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(test_url, download=False)
                logger.info("✅ yt-dlp can extract Instagram info")
                logger.info(f"Title: {info.get('title', 'Unknown')}")
                logger.info(f"Uploader: {info.get('uploader', 'Unknown')}")
                return True
            except Exception as e:
                error_msg = str(e)
                logger.error(f"❌ yt-dlp extraction failed: {error_msg}")
                
                # Анализируем ошибку
                if 'rate-limit' in error_msg.lower():
                    logger.error("🚫 Rate limit detected")
                elif 'login required' in error_msg.lower():
                    logger.error("🔐 Login required - consider using cookies")
                elif 'not available' in error_msg.lower():
                    logger.error("📵 Content not available")
                
                return False
                
    except ImportError:
        logger.error("❌ yt-dlp not available")
        return False

def check_cookies():
    """Проверяет наличие и валидность cookies"""
    logger.info("\n=== COOKIES CHECK ===")
    
    cookies_file = 'cookies/instagram.txt'
    
    if not os.path.exists(cookies_file):
        logger.warning("⚠️ No cookies file found")
        logger.info("Consider running: python get_instagram_cookies.py")
        return False
    
    try:
        with open(cookies_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        cookie_count = 0
        important_cookies = []
        
        for line in lines:
            if line.startswith('#') or not line.strip():
                continue
            
            parts = line.strip().split('\t')
            if len(parts) >= 7:
                cookie_count += 1
                cookie_name = parts[5]
                if cookie_name in ['sessionid', 'csrftoken', 'ds_user_id']:
                    important_cookies.append(cookie_name)
        
        logger.info(f"Cookies file contains {cookie_count} cookies")
        logger.info(f"Important cookies: {important_cookies}")
        
        if 'sessionid' in important_cookies:
            logger.info("✅ sessionid found - authentication available")
            return True
        else:
            logger.warning("⚠️ sessionid not found - limited access")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error reading cookies: {e}")
        return False

def generate_recommendations():
    """Генерирует рекомендации по решению проблем"""
    logger.info("\n=== RECOMMENDATIONS ===")
    
    recommendations = []
    
    # Проверяем логи ошибок
    error_log = 'logs/instagram_errors.log'
    if os.path.exists(error_log):
        try:
            with open(error_log, 'r', encoding='utf-8') as f:
                recent_errors = f.readlines()[-10:]  # Последние 10 ошибок
            
            rate_limit_count = sum(1 for line in recent_errors if 'rate-limit' in line.lower())
            
            if rate_limit_count > 0:
                recommendations.append("🔄 Rate limit detected - use cookies or proxy")
                recommendations.append("⏱️ Add delays between requests")
                recommendations.append("🔄 Rotate User-Agent strings")
        except:
            pass
    
    # Общие рекомендации
    recommendations.extend([
        "🍪 Use cookies from browser: python get_instagram_cookies.py",
        "🔄 Update yt-dlp: pip install -U yt-dlp",
        "🌐 Consider using proxy servers",
        "⏰ Add random delays between requests",
        "🔄 Rotate User-Agent headers",
        "📱 Use mobile User-Agent strings",
        "🏠 Test from different IP/location",
    ])
    
    for i, rec in enumerate(recommendations, 1):
        logger.info(f"{i}. {rec}")

def main():
    """Основная функция диагностики"""
    logger.info("Instagram Diagnostic Tool")
    logger.info("=" * 50)
    
    # Запускаем все проверки
    check_system_info()
    check_network_connectivity()
    check_ip_reputation()
    check_yt_dlp_version()
    test_instagram_access()
    test_yt_dlp_instagram()
    check_cookies()
    generate_recommendations()
    
    logger.info("\n" + "=" * 50)
    logger.info("Diagnostic complete. Check the results above.")
    logger.info("For more help, see: backend/cookies/README.md")

if __name__ == "__main__":
    main() 