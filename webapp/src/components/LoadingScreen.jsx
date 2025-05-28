import React from 'react'
import '../styles/LoadingScreen.css'

const LoadingScreen = () => {
  return (
    <div className="loading-screen">
      <div className="loading-content">
        <div className="loading-logo">
          <div className="logo-icon">🎬</div>
          <h1 className="logo-text">TimoReel</h1>
        </div>
        
        <div className="loading-spinner">
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
        </div>
        
        <p className="loading-text">Загружаем видео...</p>
      </div>
    </div>
  )
}

export default LoadingScreen 