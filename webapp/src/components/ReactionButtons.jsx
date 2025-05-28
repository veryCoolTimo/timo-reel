import React, { useState } from 'react'
import '../styles/ReactionButtons.css'

const ReactionButtons = ({ fileId, onReaction, userId }) => {
  const [likePressed, setLikePressed] = useState(false)
  const [commentPressed, setCommentPressed] = useState(false)

  const handleLike = async () => {
    if (!userId) return
    
    setLikePressed(true)
    
    try {
      await onReaction(fileId, 'like')
      
      // Анимация сердечка
      setTimeout(() => setLikePressed(false), 300)
    } catch (error) {
      console.error('Error sending like:', error)
      setLikePressed(false)
    }
  }

  const handleComment = async () => {
    if (!userId) return
    
    setCommentPressed(true)
    
    try {
      await onReaction(fileId, 'comment')
      
      // Анимация комментария
      setTimeout(() => setCommentPressed(false), 300)
    } catch (error) {
      console.error('Error sending comment:', error)
      setCommentPressed(false)
    }
  }

  return (
    <div className="reaction-buttons">
      <div className="reaction-column">
        {/* Кнопка лайка */}
        <button 
          className={`reaction-button like-button ${likePressed ? 'pressed' : ''}`}
          onClick={handleLike}
          disabled={!userId}
          aria-label="Поставить лайк"
        >
          <div className="button-icon">
            <div className="heart-icon">
              {likePressed ? '❤️' : '🤍'}
            </div>
          </div>
          <span className="button-label">Лайк</span>
        </button>

        {/* Кнопка комментария */}
        <button 
          className={`reaction-button comment-button ${commentPressed ? 'pressed' : ''}`}
          onClick={handleComment}
          disabled={!userId}
          aria-label="Оставить комментарий"
        >
          <div className="button-icon">
            <div className="comment-icon">
              💬
            </div>
          </div>
          <span className="button-label">Комментарий</span>
        </button>

        {/* Дополнительные кнопки */}
        <button 
          className="reaction-button share-button"
          onClick={() => {
            if (window.Telegram?.WebApp) {
              window.Telegram.WebApp.showAlert('Функция поделиться скоро будет доступна!')
            }
          }}
          aria-label="Поделиться"
        >
          <div className="button-icon">
            <div className="share-icon">
              📤
            </div>
          </div>
          <span className="button-label">Поделиться</span>
        </button>
      </div>

      {/* Анимированные эффекты */}
      {likePressed && (
        <div className="reaction-effect like-effect">
          <div className="floating-heart">❤️</div>
          <div className="floating-heart">❤️</div>
          <div className="floating-heart">❤️</div>
        </div>
      )}

      {commentPressed && (
        <div className="reaction-effect comment-effect">
          <div className="floating-comment">💬</div>
        </div>
      )}
    </div>
  )
}

export default ReactionButtons 