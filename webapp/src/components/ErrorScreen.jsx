import React from 'react'
import '../styles/ErrorScreen.css'

const ErrorScreen = ({ message, onRetry }) => {
  return (
    <div className="error-screen">
      <div className="error-content">
        <div className="error-icon">😔</div>
        <h2 className="error-title">Что-то пошло не так</h2>
        <p className="error-message">{message}</p>
        
        {onRetry && (
          <button className="retry-button" onClick={onRetry}>
            🔄 Попробовать снова
          </button>
        )}
      </div>
    </div>
  )
}

export default ErrorScreen 