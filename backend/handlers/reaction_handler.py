#!/usr/bin/env python3
"""
Обработчик реакций - отправка уведомлений авторам видео
"""

import logging
from telegram import Bot
from telegram.error import TelegramError
from utils.cache import get_video_author, is_user_muted, add_reaction
from utils.config import BOT_TOKEN

logger = logging.getLogger(__name__)

async def send_reaction_notification(user_id: int, file_id: str, reaction_type: str, reactor_username: str):
    """
    Отправляет уведомление автору видео о новой реакции
    
    Args:
        user_id: ID пользователя, который поставил реакцию
        file_id: ID видео файла
        reaction_type: тип реакции ('like' или 'comment')
        reactor_username: имя пользователя, который поставил реакцию
    """
    try:
        # Получаем информацию об авторе видео
        video_author = get_video_author(file_id)
        if not video_author:
            logger.warning(f"Video author not found for file_id: {file_id}")
            return False
        
        author_id = video_author['user_id']
        author_username = video_author['username']
        
        # Проверяем, не ставит ли автор реакцию на свое же видео
        if user_id == author_id:
            logger.debug(f"User {user_id} reacted to their own video, skipping notification")
            return True
        
        # Проверяем, не отключены ли уведомления у автора
        if is_user_muted(author_id):
            logger.debug(f"User {author_id} has notifications muted, skipping")
            return True
        
        # Сохраняем реакцию в базе данных
        add_reaction(user_id, file_id, reaction_type)
        
        # Формируем сообщение уведомления
        if reaction_type == 'like':
            emoji = "❤️"
            action = "поставил лайк"
        elif reaction_type == 'comment':
            emoji = "💬"
            action = "прокомментировал"
        else:
            emoji = "👍"
            action = f"отреагировал ({reaction_type})"
        
        notification_text = (
            f"{emoji} Новая реакция на ваше видео!\n\n"
            f"👤 @{reactor_username} {action} ваше видео\n"
            f"🎬 Автор: @{author_username}\n\n"
            f"💡 Чтобы отключить уведомления, используйте /mute"
        )
        
        # Отправляем уведомление автору видео
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(
            chat_id=author_id,
            text=notification_text,
            parse_mode='HTML'
        )
        
        logger.info(f"Sent {reaction_type} notification to user {author_id} from {user_id}")
        return True
        
    except TelegramError as e:
        if "chat not found" in str(e).lower() or "user not found" in str(e).lower():
            logger.warning(f"Cannot send notification to user {author_id}: user not accessible")
        else:
            logger.error(f"Telegram error sending notification to {author_id}: {e}")
        return False
        
    except Exception as e:
        logger.error(f"Error sending reaction notification: {e}")
        return False

async def process_reaction(user_id: int, file_id: str, reaction_type: str, username: str = None):
    """
    Обрабатывает реакцию пользователя
    
    Args:
        user_id: ID пользователя
        file_id: ID видео файла
        reaction_type: тип реакции
        username: имя пользователя (опционально)
    """
    try:
        # Используем username или fallback
        reactor_username = username or f"user_{user_id}"
        
        # Отправляем уведомление
        success = await send_reaction_notification(
            user_id=user_id,
            file_id=file_id,
            reaction_type=reaction_type,
            reactor_username=reactor_username
        )
        
        if success:
            logger.info(f"Successfully processed {reaction_type} from {user_id} for video {file_id}")
        else:
            logger.warning(f"Failed to process {reaction_type} from {user_id} for video {file_id}")
        
        return success
        
    except Exception as e:
        logger.error(f"Error processing reaction: {e}")
        return False 