import yt_dlp
import tempfile
import os
import logging
from typing import Optional, Dict, Any
from utils.config import MAX_VIDEO_SIZE
from .instagram_fix import (
    get_instagram_options, 
    get_fallback_options, 
    get_server_specific_config,
    add_delay_between_requests,
    is_rate_limited_error,
    log_instagram_error,
    get_cookies_options
)

logger = logging.getLogger(__name__)

class VideoDownloader:
    def __init__(self):
        # Базовые настройки для yt-dlp
        self.ydl_opts = {
            'format': 'best[filesize<50M]/best',  # Предпочитаем видео до 50MB
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
            'extractaudio': False,
            'audioformat': 'mp3',
            'embed_subs': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'quiet': True,
            'no_warnings': True,
            # Добавляем User-Agent для обхода блокировок
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            # Настройки для Instagram
            'extractor_args': {
                'instagram': {
                    'api_version': 'v1'
                }
            }
        }
        
        # Альтернативные настройки для проблемных сайтов
        self.fallback_opts = {
            'format': 'worst[filesize<50M]/worst',  # Пробуем худшее качество
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
            },
            'sleep_interval': 1,
            'max_sleep_interval': 5
        }
        
        # Счетчик запросов для Instagram
        self.instagram_request_count = 0
    
    def is_supported_url(self, url: str) -> bool:
        """Проверяет, поддерживается ли URL для загрузки"""
        supported_domains = [
            'instagram.com',
            'www.instagram.com',
            'tiktok.com',
            'www.tiktok.com',
            'vm.tiktok.com',
            'vt.tiktok.com'
        ]
        
        return any(domain in url.lower() for domain in supported_domains)
    
    def is_instagram_url(self, url: str) -> bool:
        """Проверяет, является ли URL ссылкой на Instagram"""
        return 'instagram.com' in url.lower()
    
    def get_instagram_download_options(self, url: str) -> Dict[str, Any]:
        """Получает оптимальные опции для загрузки Instagram видео"""
        
        # Используем серверную конфигурацию
        options = get_server_specific_config()
        
        # Добавляем cookies если доступны
        cookies_opts = get_cookies_options()
        options.update(cookies_opts)
        
        # Базовые настройки
        options.update({
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
            'extractaudio': False,
            'embed_subs': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'quiet': True,
        })
        
        return options

    def extract_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Извлекает информацию о видео без загрузки"""
        
        # Для Instagram используем специальные настройки
        if self.is_instagram_url(url):
            return self._extract_instagram_info(url)
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'filesize': info.get('filesize', 0),
                    'ext': info.get('ext', 'mp4'),
                    'url': url
                }
        except Exception as e:
            logger.warning(f"Primary extraction failed for {url}: {e}")
            
            # Пробуем с fallback настройками
            try:
                with yt_dlp.YoutubeDL(self.fallback_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    return {
                        'title': info.get('title', 'Unknown Video'),
                        'duration': info.get('duration', 0),
                        'uploader': info.get('uploader', 'Unknown'),
                        'filesize': info.get('filesize', 0),
                        'ext': info.get('ext', 'mp4'),
                        'url': url
                    }
            except Exception as e2:
                logger.error(f"Fallback extraction also failed for {url}: {e2}")
                return None
    
    def _extract_instagram_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Извлекает информацию о Instagram видео с улучшенной обработкой"""
        
        # Добавляем задержку между запросами
        if self.instagram_request_count > 0:
            add_delay_between_requests()
        
        self.instagram_request_count += 1
        
        # Пробуем основные настройки
        options = self.get_instagram_download_options(url)
        
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:  # Проверяем что info не None
                    return {
                        'title': info.get('title', 'Instagram Video'),
                        'duration': info.get('duration', 0),
                        'uploader': info.get('uploader', 'Instagram User'),
                        'filesize': info.get('filesize', 0),
                        'ext': info.get('ext', 'mp4'),
                        'url': url
                    }
                else:
                    logger.warning(f"Instagram returned empty info for {url}")
                    return None
        except Exception as e:
            error_msg = str(e)
            log_instagram_error(url, error_msg)
            
            # Пробуем fallback конфигурации
            if is_rate_limited_error(error_msg):
                logger.info("Rate limit detected, trying fallback configurations...")
                return self._try_instagram_fallbacks(url)
            
            return None
    
    def _try_instagram_fallbacks(self, url: str) -> Optional[Dict[str, Any]]:
        """Пробует fallback конфигурации для Instagram"""
        
        fallback_configs = get_fallback_options()
        
        for i, config in enumerate(fallback_configs):
            try:
                logger.info(f"Trying Instagram fallback config {i+1}/{len(fallback_configs)}")
                
                # Добавляем дополнительную задержку
                add_delay_between_requests()
                
                config.update({
                    'outtmpl': '%(title)s.%(ext)s',
                    'noplaylist': True,
                    'quiet': True,
                })
                
                with yt_dlp.YoutubeDL(config) as ydl:
                    info = ydl.extract_info(url, download=False)
                    logger.info(f"Instagram fallback config {i+1} succeeded")
                    return {
                        'title': info.get('title', 'Instagram Video'),
                        'duration': info.get('duration', 0),
                        'uploader': info.get('uploader', 'Instagram User'),
                        'filesize': info.get('filesize', 0),
                        'ext': info.get('ext', 'mp4'),
                        'url': url
                    }
                    
            except Exception as e:
                logger.warning(f"Instagram fallback config {i+1} failed: {e}")
                continue
        
        logger.error(f"All Instagram fallback configs failed for {url}")
        return None

    def download_video(self, url: str) -> Optional[str]:
        """
        Загружает видео во временный файл и возвращает путь к нему
        Возвращает None в случае ошибки
        """
        temp_dir = None
        success = False
        
        try:
            # Создаем временную директорию
            temp_dir = tempfile.mkdtemp()
            
            # Для Instagram используем специальную логику
            if self.is_instagram_url(url):
                success = self._download_instagram_video(url, temp_dir)
            else:
                # Пробуем основные настройки
                success = self._try_download(url, temp_dir, self.ydl_opts, "primary")
                
                if not success:
                    # Пробуем fallback настройки
                    logger.info(f"Trying fallback method for {url}")
                    success = self._try_download(url, temp_dir, self.fallback_opts, "fallback")
            
            if success:
                # Находим загруженный файл
                for file in os.listdir(temp_dir):
                    if file.endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm', '.m4v')):
                        file_path = os.path.join(temp_dir, file)
                        
                        # Проверяем размер загруженного файла
                        if os.path.getsize(file_path) > MAX_VIDEO_SIZE:
                            logger.warning(f"Downloaded file too large: {file_path}")
                            os.remove(file_path)
                            return None
                        
                        logger.info(f"Successfully downloaded: {file_path}")
                        return file_path
                
                logger.error(f"No video file found after download from {url}")
                return None
            else:
                return None
                
        except Exception as e:
            logger.error(f"Unexpected error downloading video from {url}: {e}")
            return None
        finally:
            # Очищаем временную директорию если загрузка не удалась
            if temp_dir and not success:
                try:
                    import shutil
                    shutil.rmtree(temp_dir, ignore_errors=True)
                except:
                    pass
    
    def _download_instagram_video(self, url: str, temp_dir: str) -> bool:
        """Загружает Instagram видео с улучшенной обработкой"""
        
        # Добавляем задержку между запросами
        if self.instagram_request_count > 0:
            add_delay_between_requests()
        
        self.instagram_request_count += 1
        
        # Пробуем основную конфигурацию
        options = self.get_instagram_download_options(url)
        options['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
        
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                # Сначала получаем информацию
                info = ydl.extract_info(url, download=False)
                
                # Проверяем размер файла
                filesize = info.get('filesize', 0)
                if filesize and filesize > MAX_VIDEO_SIZE:
                    logger.warning(f"Instagram video too large: {filesize} bytes > {MAX_VIDEO_SIZE}")
                    return False
                
                # Загружаем видео
                ydl.download([url])
                logger.info(f"Instagram download successful")
                return True
                
        except Exception as e:
            error_msg = str(e)
            log_instagram_error(url, error_msg)
            
            # Пробуем fallback конфигурации
            if is_rate_limited_error(error_msg):
                logger.info("Rate limit detected, trying Instagram fallback configurations...")
                return self._try_instagram_download_fallbacks(url, temp_dir)
            
            return False
    
    def _try_instagram_download_fallbacks(self, url: str, temp_dir: str) -> bool:
        """Пробует fallback конфигурации для загрузки Instagram видео"""
        
        fallback_configs = get_fallback_options()
        
        for i, config in enumerate(fallback_configs):
            try:
                logger.info(f"Trying Instagram download fallback config {i+1}/{len(fallback_configs)}")
                
                # Добавляем дополнительную задержку
                add_delay_between_requests()
                
                config['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
                
                with yt_dlp.YoutubeDL(config) as ydl:
                    # Сначала получаем информацию
                    info = ydl.extract_info(url, download=False)
                    
                    # Проверяем размер файла
                    filesize = info.get('filesize', 0)
                    if filesize and filesize > MAX_VIDEO_SIZE:
                        logger.warning(f"Instagram video too large (fallback {i+1}): {filesize} bytes > {MAX_VIDEO_SIZE}")
                        continue
                    
                    # Загружаем видео
                    ydl.download([url])
                    logger.info(f"Instagram download fallback config {i+1} succeeded")
                    return True
                    
            except Exception as e:
                logger.warning(f"Instagram download fallback config {i+1} failed: {e}")
                continue
        
        logger.error(f"All Instagram download fallback configs failed for {url}")
        return False
    
    def _try_download(self, url: str, temp_dir: str, opts: dict, method: str) -> bool:
        """Пробует загрузить видео с заданными настройками"""
        try:
            # Настройки для загрузки
            download_opts = opts.copy()
            download_opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
            
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                # Сначала получаем информацию
                info = ydl.extract_info(url, download=False)
                
                # Проверяем размер файла
                filesize = info.get('filesize', 0)
                if filesize and filesize > MAX_VIDEO_SIZE:
                    logger.warning(f"Video too large ({method}): {filesize} bytes > {MAX_VIDEO_SIZE}")
                    return False
                
                # Загружаем видео
                ydl.download([url])
                logger.info(f"Download successful with {method} method")
                return True
                
        except Exception as e:
            logger.warning(f"Download failed with {method} method for {url}: {e}")
            return False

    def cleanup_file(self, file_path: str):
        """Удаляет временный файл и его директорию"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                # Удаляем временную директорию если она пустая
                temp_dir = os.path.dirname(file_path)
                if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                    os.rmdir(temp_dir)
                logger.debug(f"Cleaned up: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up file {file_path}: {e}")

# Глобальный экземпляр загрузчика
downloader = VideoDownloader() 