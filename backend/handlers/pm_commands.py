#!/usr/bin/env python3
"""
Команды для личных сообщений с ботом
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils.cache import (
    get_user_reactions, 
    get_user_settings, 
    update_user_settings,
    is_user_muted
)

logger = logging.getLogger(__name__)

async def mute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /mute - отключить уведомления о реакциях"""
    if update.message.chat.type != 'private':
        await update.message.reply_text(
            "❌ Эта команда доступна только в личных сообщениях"
        )
        return
    
    user_id = update.effective_user.id
    
    # Обновляем настройки пользователя
    update_user_settings(user_id, {'muted': True})
    
    await update.message.reply_text(
        "🔇 Уведомления о реакциях отключены\n\n"
        "Используйте /unmute для включения уведомлений"
    )
    
    logger.info(f"User {user_id} muted notifications")

async def unmute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /unmute - включить уведомления о реакциях"""
    if update.message.chat.type != 'private':
        await update.message.reply_text(
            "❌ Эта команда доступна только в личных сообщениях"
        )
        return
    
    user_id = update.effective_user.id
    
    # Обновляем настройки пользователя
    update_user_settings(user_id, {'muted': False})
    
    await update.message.reply_text(
        "🔔 Уведомления о реакциях включены\n\n"
        "Теперь вы будете получать уведомления, когда кто-то лайкает или комментирует ваши видео"
    )
    
    logger.info(f"User {user_id} unmuted notifications")

async def likes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /likes - показать историю реакций пользователя"""
    if update.message.chat.type != 'private':
        await update.message.reply_text(
            "❌ Эта команда доступна только в личных сообщениях"
        )
        return
    
    user_id = update.effective_user.id
    
    # Получаем реакции пользователя
    reactions = get_user_reactions(user_id)
    
    if not reactions:
        await update.message.reply_text(
            "📭 У вас пока нет реакций\n\n"
            "Лайкайте и комментируйте видео в чатах, чтобы увидеть историю здесь!"
        )
        return
    
    # Формируем сообщение с историей
    message_text = f"❤️ Ваши реакции ({len(reactions)}):\n\n"
    
    for i, reaction in enumerate(reactions[-20:], 1):  # Показываем последние 20
        reaction_emoji = "❤️" if reaction['type'] == 'like' else "💬"
        timestamp = reaction.get('timestamp', 'неизвестно')
        
        message_text += f"{i}. {reaction_emoji} {reaction['type']} - {timestamp}\n"
    
    if len(reactions) > 20:
        message_text += f"\n... и еще {len(reactions) - 20} реакций"
    
    await update.message.reply_text(message_text)
    
    logger.info(f"User {user_id} requested likes history: {len(reactions)} reactions")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /status - показать статус пользователя"""
    if update.message.chat.type != 'private':
        await update.message.reply_text(
            "❌ Эта команда доступна только в личных сообщениях"
        )
        return
    
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    
    # Получаем настройки и статистику пользователя
    settings = get_user_settings(user_id)
    reactions = get_user_reactions(user_id)
    
    muted = settings.get('muted', False)
    mute_status = "🔇 Отключены" if muted else "🔔 Включены"
    
    likes_count = len([r for r in reactions if r['type'] == 'like'])
    comments_count = len([r for r in reactions if r['type'] == 'comment'])
    
    status_text = f"""
👤 Ваш статус в TimoReel

🆔 ID: {user_id}
👤 Имя: {username}

📊 Статистика:
❤️ Лайков поставлено: {likes_count}
💬 Комментариев: {comments_count}
📝 Всего реакций: {len(reactions)}

⚙️ Настройки:
🔔 Уведомления: {mute_status}

📋 Команды:
/mute - отключить уведомления
/unmute - включить уведомления  
/likes - история реакций
"""
    
    await update.message.reply_text(status_text)
    
    logger.info(f"User {user_id} requested status") 