import yt_dlp
import tempfile
import os
import logging
from typing import Optional, Dict, Any
from utils.config import MAX_VIDEO_SIZE

logger = logging.getLogger(__name__)

class VideoDownloader:
    def __init__(self):
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
        }
    
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
    
    def extract_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Извлекает информацию о видео без загрузки"""
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
            logger.error(f"Error extracting info from {url}: {e}")
            return None
    
    def download_video(self, url: str) -> Optional[str]:
        """
        Загружает видео во временный файл и возвращает путь к нему
        Возвращает None в случае ошибки
        """
        try:
            # Создаем временную директорию
            temp_dir = tempfile.mkdtemp()
            
            # Настройки для загрузки
            download_opts = self.ydl_opts.copy()
            download_opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
            
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                # Сначала получаем информацию
                info = ydl.extract_info(url, download=False)
                
                # Проверяем размер файла
                filesize = info.get('filesize', 0)
                if filesize and filesize > MAX_VIDEO_SIZE:
                    logger.warning(f"Video too large: {filesize} bytes > {MAX_VIDEO_SIZE}")
                    return None
                
                # Загружаем видео
                ydl.download([url])
                
                # Находим загруженный файл
                for file in os.listdir(temp_dir):
                    if file.endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
                        file_path = os.path.join(temp_dir, file)
                        
                        # Проверяем размер загруженного файла
                        if os.path.getsize(file_path) > MAX_VIDEO_SIZE:
                            logger.warning(f"Downloaded file too large: {file_path}")
                            os.remove(file_path)
                            return None
                        
                        return file_path
                
                logger.error(f"No video file found after download from {url}")
                return None
                
        except Exception as e:
            logger.error(f"Error downloading video from {url}: {e}")
            return None
    
    def cleanup_file(self, file_path: str):
        """Удаляет временный файл и его директорию"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                # Удаляем временную директорию если она пустая
                temp_dir = os.path.dirname(file_path)
                if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                    os.rmdir(temp_dir)
        except Exception as e:
            logger.error(f"Error cleaning up file {file_path}: {e}")

# Глобальный экземпляр загрузчика
downloader = VideoDownloader() 