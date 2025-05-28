import React from 'react'
import '../styles/EmptyState.css'

const EmptyState = () => {
  return (
    <div className="empty-state">
      <div className="empty-content">
        <div className="empty-icon">📱</div>
        <h2 className="empty-title">Пока нет видео</h2>
        <p className="empty-message">
          Отправьте ссылку на видео из Instagram или TikTok в чат, 
          и оно появится здесь!
        </p>
        
        <div className="empty-examples">
          <div className="example-item">
            <span className="example-icon">📸</span>
            <span>Instagram Reels</span>
          </div>
          <div className="example-item">
            <span className="example-icon">🎵</span>
            <span>TikTok видео</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default EmptyState 