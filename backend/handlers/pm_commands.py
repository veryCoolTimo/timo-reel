import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils.cache import (
    set_user_mute_status, 
    is_user_muted, 
    get_user_reactions,
    load_metadata
)

logger = logging.getLogger(__name__)

async def mute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /mute - отключает уведомления о реакциях"""
    if update.message.chat.type != 'private':
        await update.message.reply_text(
            "❌ Эта команда доступна только в личных сообщениях с ботом."
        )
        return
    
    user_id = update.effective_user.id
    
    # Устанавливаем статус mute
    set_user_mute_status(user_id, True)
    
    await update.message.reply_text(
        "🔇 Уведомления о реакциях отключены.\n"
        "Используйте /unmute чтобы включить их обратно."
    )
    
    logger.info(f"User {user_id} muted notifications")

async def unmute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /unmute - включает уведомления о реакциях"""
    if update.message.chat.type != 'private':
        await update.message.reply_text(
            "❌ Эта команда доступна только в личных сообщениях с ботом."
        )
        return
    
    user_id = update.effective_user.id
    
    # Снимаем статус mute
    set_user_mute_status(user_id, False)
    
    await update.message.reply_text(
        "🔔 Уведомления о реакциях включены.\n"
        "Теперь вы будете получать сообщения о лайках и комментариях к вашим видео."
    )
    
    logger.info(f"User {user_id} unmuted notifications")

async def likes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /likes - показывает последние реакции пользователя"""
    if update.message.chat.type != 'private':
        await update.message.reply_text(
            "❌ Эта команда доступна только в личных сообщениях с ботом."
        )
        return
    
    user_id = update.effective_user.id
    
    # Получаем реакции пользователя
    reactions = get_user_reactions(user_id)
    
    if not reactions:
        await update.message.reply_text(
            "📭 У вас пока нет реакций.\n"
            "Ставьте лайки и комментарии к видео в WebApp!"
        )
        return
    
    # Ограничиваем до последних 20 реакций
    recent_reactions = reactions[-20:]
    
    # Получаем информацию о видео
    metadata = load_metadata()
    videos = metadata.get("videos", {})
    
    response_lines = ["📊 Ваши последние реакции:\n"]
    
    for reaction in reversed(recent_reactions):  # Показываем новые сначала
        file_id = reaction["file_id"]
        reaction_type = reaction["type"]
        timestamp = reaction["timestamp"]
        
        # Ищем информацию о видео
        video_info = videos.get(file_id)
        if video_info:
            username = video_info.get("username", "Unknown")
            emoji = "❤️" if reaction_type == "like" else "💬"
            response_lines.append(f"{emoji} Видео от @{username}")
        else:
            emoji = "❤️" if reaction_type == "like" else "💬"
            response_lines.append(f"{emoji} Видео (удалено)")
    
    response_text = "\n".join(response_lines)
    
    # Telegram имеет ограничение на длину сообщения
    if len(response_text) > 4000:
        response_text = response_text[:4000] + "\n\n... (показаны не все реакции)"
    
    await update.message.reply_text(response_text)
    
    logger.info(f"User {user_id} requested likes history ({len(recent_reactions)} reactions)")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /status - показывает статус пользователя"""
    if update.message.chat.type != 'private':
        await update.message.reply_text(
            "❌ Эта команда доступна только в личных сообщениях с ботом."
        )
        return
    
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    
    # Проверяем статус уведомлений
    is_muted = is_user_muted(user_id)
    mute_status = "🔇 Отключены" if is_muted else "🔔 Включены"
    
    # Считаем количество реакций
    reactions = get_user_reactions(user_id)
    total_reactions = len(reactions)
    likes_count = len([r for r in reactions if r["type"] == "like"])
    comments_count = len([r for r in reactions if r["type"] == "comment"])
    
    status_text = f"""
👤 Ваш статус в TimoReel

🆔 ID: {user_id}
👤 Имя: @{username}

📊 Статистика:
• Всего реакций: {total_reactions}
• Лайков: {likes_count} ❤️
• Комментариев: {comments_count} 💬

🔔 Уведомления: {mute_status}

⚙️ Команды:
/mute - отключить уведомления
/unmute - включить уведомления  
/likes - показать историю реакций
/status - показать этот статус
"""
    
    await update.message.reply_text(status_text)
    
    logger.info(f"User {user_id} requested status") 