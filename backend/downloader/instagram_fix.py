#!/usr/bin/env python3
"""
Instagram Fix для серверов
Решение проблем с rate-limit и блокировками Instagram
"""

import os
import random
import time
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

# User-Agent строки для ротации
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
]

# Прокси серверы (можно добавить свои)
PROXY_LIST = [
    # Добавьте сюда ваши прокси в формате: 'http://user:pass@host:port'
    # 'http://proxy1.example.com:8080',
    # 'http://proxy2.example.com:8080',
]

def get_instagram_options() -> Dict[str, any]:
    """Получает оптимальные опции для yt-dlp для Instagram"""
    
    # Базовые опции
    options = {
        'format': 'best[height<=720]',  # Ограничиваем качество для скорости
        'no_warnings': True,
        'extract_flat': False,
        'writethumbnail': False,
        'writeinfojson': False,
        'ignoreerrors': True,
        'no_check_certificate': True,
        'prefer_insecure': True,
        'socket_timeout': 30,
        'retries': 3,
        'fragment_retries': 3,
        'skip_unavailable_fragments': True,
    }
    
    # Ротация User-Agent
    options['http_headers'] = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
    }
    
    # Добавляем прокси если доступны
    if PROXY_LIST:
        proxy = random.choice(PROXY_LIST)
        options['proxy'] = proxy
        logger.info(f"Using proxy: {proxy}")
    
    # Добавляем задержки для избежания rate-limit
    options['sleep_interval'] = random.uniform(1, 3)
    options['max_sleep_interval'] = 5
    
    return options

def get_fallback_options() -> List[Dict[str, any]]:
    """Получает список fallback опций для повторных попыток"""
    
    fallback_configs = []
    
    # Конфиг 1: Минимальное качество с мобильным UA
    config1 = get_instagram_options()
    config1.update({
        'format': 'worst',
        'socket_timeout': 120,
        'retries': 10,
        'sleep_interval': random.uniform(8, 15),
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.1 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    })
    fallback_configs.append(config1)
    
    # Конфиг 2: Старый Android браузер
    config2 = get_instagram_options()
    config2.update({
        'format': 'worst[height<=480]',
        'socket_timeout': 150,
        'retries': 15,
        'sleep_interval': random.uniform(10, 20),
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip',
            'Connection': 'keep-alive',
        }
    })
    fallback_configs.append(config2)
    
    # Конфиг 3: Desktop Firefox с прокси эмуляцией
    config3 = get_instagram_options()
    config3.update({
        'format': 'worst',
        'socket_timeout': 180,
        'retries': 20,
        'sleep_interval': random.uniform(15, 25),
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Via': '1.1 proxy.example.com:8080',
            'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        }
    })
    fallback_configs.append(config3)
    
    # Конфиг 4: Старый Safari (максимальная совместимость)
    config4 = get_instagram_options()
    config4.update({
        'format': 'worst[filesize<10M]',
        'socket_timeout': 200,
        'retries': 25,
        'sleep_interval': random.uniform(20, 30),
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        },
        'prefer_insecure': True,
        'no_check_certificate': True,
    })
    fallback_configs.append(config4)
    
    return fallback_configs

def add_delay_between_requests():
    """Добавляет случайную задержку между запросами"""
    delay = random.uniform(2, 5)
    logger.info(f"Adding delay: {delay:.2f} seconds")
    time.sleep(delay)

def is_rate_limited_error(error_msg: str) -> bool:
    """Проверяет, является ли ошибка rate-limit"""
    rate_limit_indicators = [
        'rate-limit reached',
        'login required',
        'Requested content is not available',
        'Too Many Requests',
        '429',
        'temporarily blocked',
    ]
    
    return any(indicator.lower() in error_msg.lower() for indicator in rate_limit_indicators)

def get_server_specific_config() -> Dict[str, any]:
    """Получает конфигурацию специфичную для сервера"""
    
    # Определяем тип окружения
    is_server = os.path.exists('/etc/os-release') or os.path.exists('/proc/version')
    
    config = get_instagram_options()
    
    if is_server:
        logger.info("Detected server environment, applying server-specific settings")
        
        # Более агрессивные настройки для серверов
        config.update({
            'socket_timeout': 120,  # Увеличено с 60
            'retries': 10,          # Увеличено с 5
            'fragment_retries': 10, # Увеличено с 5
            'sleep_interval': random.uniform(5, 12),  # Увеличено с 3-6
            'max_sleep_interval': 20,                 # Увеличено с 10
            'sleep_interval_requests': random.uniform(2, 5),
            'sleep_interval_subtitles': random.uniform(1, 3),
        })
        
        # Специальные заголовки для серверов (имитация мобильного браузера)
        config['http_headers'].update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.1 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'X-Real-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'X-Requested-With': 'XMLHttpRequest',
        })
        
        # Дополнительные настройки для серверов
        config.update({
            'prefer_insecure': True,
            'no_check_certificate': True,
            'call_home': False,
            'no_color': True,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'extractor_retries': 5,
        })
    
    return config

def log_instagram_error(url: str, error_msg: str):
    """Логирует ошибки Instagram с рекомендациями"""
    
    logger.error(f"Instagram download failed for {url}: {error_msg}")
    
    if is_rate_limited_error(error_msg):
        logger.warning("Rate limit detected. Recommendations:")
        logger.warning("1. Add delays between requests")
        logger.warning("2. Use proxy servers")
        logger.warning("3. Rotate User-Agent strings")
        logger.warning("4. Consider using cookies from browser")
    
    # Статистика ошибок
    error_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'instagram_errors.log')
    try:
        # Создаем директорию logs если не существует
        os.makedirs(os.path.dirname(error_file), exist_ok=True)
        
        with open(error_file, 'a', encoding='utf-8') as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {url} - {error_msg}\n")
    except Exception as e:
        logger.error(f"Could not write to error log: {e}")

def get_cookies_options() -> Dict[str, any]:
    """Получает опции для использования cookies (если доступны)"""
    
    cookies_file = os.path.join(os.path.dirname(__file__), '..', 'cookies', 'instagram.txt')
    
    options = {}
    
    if os.path.exists(cookies_file):
        options['cookiefile'] = cookies_file
        logger.info("Using cookies file for Instagram")
    else:
        logger.info("No cookies file found, using cookieless mode")
    
    return options 