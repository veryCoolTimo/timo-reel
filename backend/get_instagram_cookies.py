#!/usr/bin/env python3
"""
Скрипт для получения Instagram cookies из браузера
Помогает решить проблемы с rate-limit на серверах
"""

import os
import sys
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def install_browser_cookie3():
    """Устанавливает browser_cookie3 если не установлен"""
    try:
        import browser_cookie3
        return True
    except ImportError:
        logger.info("Installing browser_cookie3...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'browser_cookie3'])
            import browser_cookie3
            return True
        except Exception as e:
            logger.error(f"Failed to install browser_cookie3: {e}")
            return False

def get_cookies_from_browser(browser_name='chrome'):
    """Получает cookies из указанного браузера"""
    try:
        import browser_cookie3
        
        # Получаем функцию для браузера
        browser_functions = {
            'chrome': browser_cookie3.chrome,
            'firefox': browser_cookie3.firefox,
            'safari': browser_cookie3.safari,
            'edge': browser_cookie3.edge,
            'opera': browser_cookie3.opera,
        }
        
        if browser_name not in browser_functions:
            logger.error(f"Unsupported browser: {browser_name}")
            return None
        
        logger.info(f"Getting cookies from {browser_name}...")
        
        # Получаем cookies для Instagram
        cookies = browser_functions[browser_name](domain_name='instagram.com')
        
        instagram_cookies = []
        for cookie in cookies:
            if 'instagram.com' in cookie.domain:
                instagram_cookies.append(cookie)
        
        if not instagram_cookies:
            logger.warning(f"No Instagram cookies found in {browser_name}")
            return None
        
        logger.info(f"Found {len(instagram_cookies)} Instagram cookies in {browser_name}")
        return instagram_cookies
        
    except Exception as e:
        logger.error(f"Error getting cookies from {browser_name}: {e}")
        return None

def save_cookies_to_file(cookies, filename='cookies/instagram.txt'):
    """Сохраняет cookies в файл в формате Netscape"""
    try:
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Netscape HTTP Cookie File\n")
            f.write(f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# This file contains Instagram cookies for yt-dlp\n\n")
            
            for cookie in cookies:
                # Формат Netscape: domain, domain_specified, path, secure, expires, name, value
                domain = cookie.domain
                domain_specified = "TRUE" if domain.startswith('.') else "FALSE"
                path = cookie.path or "/"
                secure = "TRUE" if cookie.secure else "FALSE"
                expires = str(int(cookie.expires)) if cookie.expires else "0"
                name = cookie.name
                value = cookie.value
                
                line = f"{domain}\t{domain_specified}\t{path}\t{secure}\t{expires}\t{name}\t{value}\n"
                f.write(line)
        
        logger.info(f"Cookies saved to {filename}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving cookies to file: {e}")
        return False

def test_cookies_file(filename='cookies/instagram.txt'):
    """Проверяет корректность cookies файла"""
    try:
        if not os.path.exists(filename):
            logger.error(f"Cookies file not found: {filename}")
            return False
        
        with open(filename, 'r', encoding='utf-8') as f:
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
        logger.info(f"Important cookies found: {important_cookies}")
        
        if 'sessionid' in important_cookies:
            logger.info("✅ sessionid found - authentication should work")
        else:
            logger.warning("⚠️ sessionid not found - may need to login to Instagram first")
        
        return cookie_count > 0
        
    except Exception as e:
        logger.error(f"Error testing cookies file: {e}")
        return False

def main():
    """Основная функция"""
    logger.info("Instagram Cookies Extractor")
    logger.info("=" * 40)
    
    # Устанавливаем browser_cookie3 если нужно
    if not install_browser_cookie3():
        logger.error("Cannot proceed without browser_cookie3")
        return False
    
    # Список браузеров для попытки
    browsers = ['chrome', 'firefox', 'safari', 'edge']
    
    cookies = None
    successful_browser = None
    
    # Пробуем каждый браузер
    for browser in browsers:
        logger.info(f"Trying {browser}...")
        cookies = get_cookies_from_browser(browser)
        if cookies:
            successful_browser = browser
            break
    
    if not cookies:
        logger.error("No Instagram cookies found in any browser")
        logger.info("Make sure you are logged into Instagram in your browser")
        return False
    
    # Сохраняем cookies
    if save_cookies_to_file(cookies):
        logger.info(f"✅ Successfully extracted cookies from {successful_browser}")
        
        # Тестируем файл
        if test_cookies_file():
            logger.info("✅ Cookies file is valid")
            logger.info("\nNext steps:")
            logger.info("1. Restart your bot to use the new cookies")
            logger.info("2. Check logs for 'Using cookies file for Instagram'")
            logger.info("3. Test Instagram video download")
            return True
        else:
            logger.error("❌ Cookies file validation failed")
            return False
    else:
        logger.error("❌ Failed to save cookies")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 