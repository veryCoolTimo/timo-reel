#!/usr/bin/env python3
"""
Демо-обработчик для тестирования функционала без реального скачивания видео
"""

import logging
import os
import shutil
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from utils.cache import add_video_metadata

logger = logging.getLogger(__name__)

# Путь к демо-видео
DEMO_VIDEO_PATH = os.path.join(os.path.dirname(__file__), '..', 'demo_video.mp4')

def create_demo_video():
    """Создает демо-видео файл если его нет"""
    if not os.path.exists(DEMO_VIDEO_PATH):
        # Создаем простой демо-файл (заглушку)
        demo_content = b"DEMO VIDEO FILE - This is a placeholder for testing TimoReel functionality"
        with open(DEMO_VIDEO_PATH, 'wb') as f:
            f.write(demo_content)
        logger.info(f"Created demo video file: {DEMO_VIDEO_PATH}")

async def handle_demo_download(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
    """Обрабатывает демо-загрузку видео"""
    message = update.message
    chat_id = message.chat_id
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    try:
        # Показываем, что бот печатает
        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_VIDEO)
        
        # Определяем платформу
        if 'instagram.com' in url:
            platform = "Instagram"
            demo_title = "Demo Instagram Reel"
            demo_author = "demo_user"
        elif 'tiktok.com' in url or 'vm.tiktok.com' in url:
            platform = "TikTok"
            demo_title = "Demo TikTok Video"
            demo_author = "demo_creator"
        else:
            platform = "Unknown"
            demo_title = "Demo Video"
            demo_author = "demo_user"
        
        # Отправляем сообщение о начале загрузки
        status_message = await message.reply_text(
            f"🎬 ДЕМО-РЕЖИМ\n\n"
            f"⬇️ Загружаю видео с {platform}...\n"
            f"📹 {demo_title}\n"
            f"👤 {demo_author}\n\n"
            f"ℹ️ Это демонстрация интерфейса"
        )
        
        # Имитируем загрузку
        import asyncio
        await asyncio.sleep(2)
        
        # Обновляем статус
        await status_message.edit_text(
            f"🎬 ДЕМО-РЕЖИМ\n\n"
            f"📤 Отправляю демо-видео...\n"
            f"📹 {demo_title}\n"
            f"👤 {demo_author}"
        )
        
        # Создаем демо-видео если его нет
        create_demo_video()
        
        # Отправляем демо-видео
        with open(DEMO_VIDEO_PATH, 'rb') as video_file:
            sent_message = await context.bot.send_video(
                chat_id=chat_id,
                video=video_file,
                caption=(
                    f"🎬 {demo_title} (ДЕМО)\n"
                    f"👤 @{username}\n"
                    f"🔗 Источник: {platform}\n\n"
                    f"ℹ️ Это демонстрация функционала TimoReel.\n"
                    f"В реальном режиме здесь было бы настоящее видео."
                ),
                reply_to_message_id=message.message_id,
                supports_streaming=True
            )
        
        # Удаляем статусное сообщение
        await status_message.delete()
        
        # Сохраняем метаданные
        if sent_message.video:
            file_id = sent_message.video.file_id
            add_video_metadata(
                file_id=file_id,
                chat_id=chat_id,
                user_id=user_id,
                username=username
            )
            logger.info(f"Demo video saved with file_id: {file_id}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in demo download for {url}: {e}")
        await message.reply_text(
            f"❌ Ошибка в демо-режиме\n\n"
            f"🔧 Проверьте настройки бота"
        )
        return False 