import React from 'react'
import '../styles/VideoOverlay.css'

const VideoOverlay = ({ username, timestamp, isVisible }) => {
  if (!isVisible) return null

  // Генерируем аватар на основе имени пользователя
  const getAvatarColor = (name) => {
    const colors = [
      '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
      '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'
    ]
    const index = name.charCodeAt(0) % colors.length
    return colors[index]
  }

  const getInitials = (name) => {
    if (!name) return '?'
    return name.charAt(0).toUpperCase()
  }

  return (
    <div className="video-overlay">
      <div className="user-info">
        <div 
          className="user-avatar"
          style={{ backgroundColor: getAvatarColor(username || 'Unknown') }}
        >
          {getInitials(username)}
        </div>
        
        <div className="user-details">
          <div className="username">
            @{username || 'Unknown'}
          </div>
          <div className="timestamp">
            {timestamp}
          </div>
        </div>
      </div>
      
      {/* Дополнительная информация */}
      <div className="video-meta">
        <div className="video-source">
          📱 TimoReel
        </div>
      </div>
    </div>
  )
}

export default VideoOverlay 