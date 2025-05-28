import React, { forwardRef, useRef, useState, useEffect } from 'react'
import VideoOverlay from './VideoOverlay'
import ReactionButtons from './ReactionButtons'
import '../styles/VideoPlayer.css'

const VideoPlayer = forwardRef(({ video, isActive, onReaction, userId }, ref) => {
  const videoRef = useRef(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [isMuted, setIsMuted] = useState(true)
  const [showControls, setShowControls] = useState(false)

  // Передаем ref наружу для управления воспроизведением
  React.useImperativeHandle(ref, () => ({
    play: () => {
      if (videoRef.current) {
        videoRef.current.play()
        setIsPlaying(true)
      }
    },
    pause: () => {
      if (videoRef.current) {
        videoRef.current.pause()
        setIsPlaying(false)
      }
    }
  }))

  useEffect(() => {
    const video = videoRef.current
    if (!video) return

    const handlePlay = () => setIsPlaying(true)
    const handlePause = () => setIsPlaying(false)
    const handleEnded = () => setIsPlaying(false)

    video.addEventListener('play', handlePlay)
    video.addEventListener('pause', handlePause)
    video.addEventListener('ended', handleEnded)

    return () => {
      video.removeEventListener('play', handlePlay)
      video.removeEventListener('pause', handlePause)
      video.removeEventListener('ended', handleEnded)
    }
  }, [])

  const handleVideoClick = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause()
      } else {
        videoRef.current.play()
      }
    }
  }

  const handleMuteToggle = () => {
    if (videoRef.current) {
      videoRef.current.muted = !isMuted
      setIsMuted(!isMuted)
    }
  }

  const handleControlsToggle = () => {
    setShowControls(!showControls)
    // Автоматически скрываем через 3 секунды
    if (!showControls) {
      setTimeout(() => setShowControls(false), 3000)
    }
  }

  const formatTime = (timestamp) => {
    const date = new Date(timestamp * 1000)
    const now = new Date()
    const diff = now - date
    
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)
    
    if (days > 0) return `${days}д назад`
    if (hours > 0) return `${hours}ч назад`
    if (minutes > 0) return `${minutes}м назад`
    return 'только что'
  }

  // Для демонстрации используем placeholder видео
  // В реальном приложении здесь будет URL видео из Telegram
  const videoUrl = `https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4`

  return (
    <div className="video-player">
      <div className="video-wrapper" onClick={handleVideoClick}>
        <video
          ref={videoRef}
          className="video-element"
          src={videoUrl}
          loop
          muted={isMuted}
          playsInline
          preload="metadata"
        />
        
        {/* Индикатор воспроизведения */}
        {!isPlaying && (
          <div className="play-indicator">
            <div className="play-button">▶</div>
          </div>
        )}
        
        {/* Градиентный оверлей */}
        <div className="video-gradient" />
      </div>

      {/* Информация о видео */}
      <VideoOverlay
        username={video.username}
        timestamp={formatTime(video.timestamp)}
        isVisible={true}
      />

      {/* Кнопки реакций */}
      <ReactionButtons
        fileId={video.file_id}
        onReaction={onReaction}
        userId={userId}
      />

      {/* Контролы звука */}
      <div className="audio-controls">
        <button 
          className={`mute-button ${isMuted ? 'muted' : 'unmuted'}`}
          onClick={handleMuteToggle}
          aria-label={isMuted ? 'Включить звук' : 'Выключить звук'}
        >
          {isMuted ? '🔇' : '🔊'}
        </button>
      </div>

      {/* Дополнительные контролы (показываются по тапу) */}
      {showControls && (
        <div className="video-controls">
          <div className="controls-overlay">
            <button onClick={handleControlsToggle} className="close-controls">
              ✕
            </button>
            <div className="video-info">
              <p>Видео от @{video.username}</p>
              <p>{formatTime(video.timestamp)}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
})

VideoPlayer.displayName = 'VideoPlayer'

export default VideoPlayer 