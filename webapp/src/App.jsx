import React, { useState, useEffect } from 'react'
import VideoFeed from './components/VideoFeed'
import LoadingScreen from './components/LoadingScreen'
import ErrorScreen from './components/ErrorScreen'
import { fetchVideoFeed } from './api'
import './styles/App.css'

function App() {
  const [videos, setVideos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [chatId, setChatId] = useState(null)
  const [userId, setUserId] = useState(null)

  useEffect(() => {
    // Получаем параметры от Telegram WebApp
    const initTelegramWebApp = () => {
      if (window.Telegram?.WebApp) {
        const tg = window.Telegram.WebApp
        tg.ready()
        
        // Получаем данные пользователя и чата
        const initData = tg.initDataUnsafe
        if (initData.user) {
          setUserId(initData.user.id)
        }
        
        // Для тестирования используем фиксированный chat_id
        // В реальном приложении это будет передаваться через start_param
        const testChatId = initData.start_param || '123456789'
        setChatId(parseInt(testChatId))
        
        // Настраиваем тему
        tg.setHeaderColor('#000000')
        tg.setBackgroundColor('#000000')
        
        console.log('Telegram WebApp initialized:', {
          user: initData.user,
          chat_id: testChatId
        })
      } else {
        // Режим разработки - используем тестовые данные
        console.log('Development mode - using test data')
        setUserId(123456789)
        setChatId(123456789)
      }
    }

    initTelegramWebApp()
  }, [])

  useEffect(() => {
    if (chatId) {
      loadVideos()
    }
  }, [chatId])

  const loadVideos = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const data = await fetchVideoFeed(chatId)
      setVideos(data.videos || [])
      
      console.log(`Loaded ${data.videos?.length || 0} videos for chat ${chatId}`)
    } catch (err) {
      console.error('Error loading videos:', err)
      setError('Не удалось загрузить видео. Попробуйте позже.')
    } finally {
      setLoading(false)
    }
  }

  const handleReaction = async (fileId, type) => {
    if (!userId) {
      console.error('User ID not available')
      return
    }

    try {
      // Отправляем реакцию через API
      const response = await fetch('/api/react', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          file_id: fileId,
          type: type
        })
      })

      if (response.ok) {
        console.log(`Reaction ${type} sent for video ${fileId}`)
        
        // Показываем уведомление через Telegram WebApp
        if (window.Telegram?.WebApp) {
          const message = type === 'like' ? '❤️ Лайк отправлен!' : '💬 Комментарий отправлен!'
          window.Telegram.WebApp.showAlert(message)
        }
      } else {
        throw new Error('Failed to send reaction')
      }
    } catch (err) {
      console.error('Error sending reaction:', err)
      if (window.Telegram?.WebApp) {
        window.Telegram.WebApp.showAlert('Ошибка отправки реакции')
      }
    }
  }

  if (loading) {
    return <LoadingScreen />
  }

  if (error) {
    return <ErrorScreen message={error} onRetry={loadVideos} />
  }

  return (
    <div className="app">
      <VideoFeed 
        videos={videos} 
        onReaction={handleReaction}
        userId={userId}
      />
    </div>
  )
}

export default App 