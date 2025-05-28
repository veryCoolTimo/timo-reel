#!/usr/bin/env python3
"""
TimoReel - Background Runner
Скрипт для запуска бота и API сервера в фоновом режиме
"""

import subprocess
import sys
import os
import time
import signal
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# PID файлы для отслеживания процессов
PID_DIR = os.path.join(os.path.dirname(__file__), 'pids')
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
BOT_PID_FILE = os.path.join(PID_DIR, 'bot.pid')
API_PID_FILE = os.path.join(PID_DIR, 'api.pid')
BOT_LOG_FILE = os.path.join(LOG_DIR, 'bot.log')
API_LOG_FILE = os.path.join(LOG_DIR, 'api.log')

def ensure_pid_dir():
    """Создает директорию для PID файлов"""
    if not os.path.exists(PID_DIR):
        os.makedirs(PID_DIR)

def ensure_log_dir():
    """Создает директорию для лог файлов"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def save_pid(pid_file: str, pid: int):
    """Сохраняет PID процесса в файл"""
    ensure_pid_dir()
    with open(pid_file, 'w') as f:
        f.write(str(pid))

def read_pid(pid_file: str) -> int:
    """Читает PID из файла"""
    if not os.path.exists(pid_file):
        return None
    try:
        with open(pid_file, 'r') as f:
            return int(f.read().strip())
    except:
        return None

def is_process_running(pid: int) -> bool:
    """Проверяет, запущен ли процесс"""
    if not pid:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def stop_process(pid_file: str, name: str):
    """Останавливает процесс по PID файлу"""
    pid = read_pid(pid_file)
    if pid and is_process_running(pid):
        try:
            os.kill(pid, signal.SIGTERM)
            logger.info(f"Stopped {name} (PID: {pid})")
            time.sleep(2)
            
            # Если процесс все еще работает, принудительно завершаем
            if is_process_running(pid):
                os.kill(pid, signal.SIGKILL)
                logger.info(f"Force killed {name} (PID: {pid})")
        except OSError as e:
            logger.error(f"Error stopping {name}: {e}")
    
    # Удаляем PID файл
    if os.path.exists(pid_file):
        os.remove(pid_file)

def start_background():
    """Запускает бота и API сервер в фоновом режиме"""
    logger.info("Starting TimoReel in background mode...")
    
    # Создаем директории
    ensure_pid_dir()
    ensure_log_dir()
    
    # Проверяем, не запущены ли уже процессы
    bot_pid = read_pid(BOT_PID_FILE)
    api_pid = read_pid(API_PID_FILE)
    
    if bot_pid and is_process_running(bot_pid):
        logger.warning(f"Bot already running (PID: {bot_pid})")
    else:
        # Запускаем бота
        logger.info("Starting Telegram bot...")
        with open(BOT_LOG_FILE, 'w') as bot_log:
            bot_process = subprocess.Popen(
                [sys.executable, 'bot.py'],
                stdout=bot_log,
                stderr=subprocess.STDOUT
            )
        save_pid(BOT_PID_FILE, bot_process.pid)
        logger.info(f"Bot started (PID: {bot_process.pid})")
        logger.info(f"Bot logs: {BOT_LOG_FILE}")
    
    if api_pid and is_process_running(api_pid):
        logger.warning(f"API server already running (PID: {api_pid})")
    else:
        # Запускаем API сервер
        logger.info("Starting API server...")
        with open(API_LOG_FILE, 'w') as api_log:
            api_process = subprocess.Popen(
                [sys.executable, 'api_server.py'],
                stdout=api_log,
                stderr=subprocess.STDOUT
            )
        save_pid(API_PID_FILE, api_process.pid)
        logger.info(f"API server started (PID: {api_process.pid})")
        logger.info(f"API logs: {API_LOG_FILE}")
    
    logger.info("TimoReel started in background mode!")
    logger.info("To stop: python run_background.py stop")
    logger.info("To check status: python run_background.py status")
    logger.info("To view logs: tail -f logs/bot.log logs/api.log")

def stop_background():
    """Останавливает все фоновые процессы"""
    logger.info("Stopping TimoReel background processes...")
    
    stop_process(BOT_PID_FILE, "Bot")
    stop_process(API_PID_FILE, "API Server")
    
    logger.info("All processes stopped")

def status():
    """Показывает статус процессов"""
    logger.info("TimoReel Status:")
    
    bot_pid = read_pid(BOT_PID_FILE)
    api_pid = read_pid(API_PID_FILE)
    
    if bot_pid and is_process_running(bot_pid):
        logger.info(f"✅ Bot running (PID: {bot_pid})")
    else:
        logger.info("❌ Bot not running")
    
    if api_pid and is_process_running(api_pid):
        logger.info(f"✅ API Server running (PID: {api_pid})")
    else:
        logger.info("❌ API Server not running")

def cleanup_pid_files():
    """Очищает устаревшие PID файлы"""
    for pid_file in [BOT_PID_FILE, API_PID_FILE]:
        if os.path.exists(pid_file):
            pid = read_pid(pid_file)
            if not pid or not is_process_running(pid):
                os.remove(pid_file)

def main():
    """Основная функция"""
    if len(sys.argv) < 2:
        print("Usage: python run_background.py [start|stop|status|restart]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # Очищаем устаревшие PID файлы
    cleanup_pid_files()
    
    if command == 'start':
        start_background()
    elif command == 'stop':
        stop_background()
    elif command == 'status':
        status()
    elif command == 'restart':
        stop_background()
        time.sleep(3)
        start_background()
    else:
        print("Invalid command. Use: start, stop, status, or restart")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        stop_background()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1) 