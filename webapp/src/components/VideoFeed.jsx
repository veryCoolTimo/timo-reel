import React, { useState, useRef, useEffect } from 'react'
import VideoPlayer from './VideoPlayer'
import EmptyState from './EmptyState'
import '../styles/VideoFeed.css'

const VideoFeed = ({ videos, onReaction, userId }) => {
  const [currentVideoIndex, setCurrentVideoIndex] = useState(0)
  const containerRef = useRef(null)
  const videoRefs = useRef([])

  useEffect(() => {
    // Настраиваем refs для видео
    videoRefs.current = videoRefs.current.slice(0, videos.length)
  }, [videos])

  useEffect(() => {
    // Автоматически воспроизводим текущее видео
    if (videoRefs.current[currentVideoIndex]) {
      videoRefs.current[currentVideoIndex].play?.()
    }

    // Паузим остальные видео
    videoRefs.current.forEach((ref, index) => {
      if (index !== currentVideoIndex && ref) {
        ref.pause?.()
      }
    })
  }, [currentVideoIndex])

  const handleScroll = (e) => {
    const container = e.target
    const scrollTop = container.scrollTop
    const itemHeight = container.clientHeight
    const newIndex = Math.round(scrollTop / itemHeight)
    
    if (newIndex !== currentVideoIndex && newIndex >= 0 && newIndex < videos.length) {
      setCurrentVideoIndex(newIndex)
    }
  }

  const scrollToVideo = (index) => {
    if (containerRef.current) {
      const itemHeight = containerRef.current.clientHeight
      containerRef.current.scrollTo({
        top: index * itemHeight,
        behavior: 'smooth'
      })
    }
  }

  const handlePrevious = () => {
    if (currentVideoIndex > 0) {
      scrollToVideo(currentVideoIndex - 1)
    }
  }

  const handleNext = () => {
    if (currentVideoIndex < videos.length - 1) {
      scrollToVideo(currentVideoIndex + 1)
    }
  }

  if (!videos || videos.length === 0) {
    return <EmptyState />
  }

  return (
    <div className="video-feed">
      <div 
        className="video-container"
        ref={containerRef}
        onScroll={handleScroll}
      >
        {videos.map((video, index) => (
          <div key={video.file_id} className="video-item">
            <VideoPlayer
              ref={el => videoRefs.current[index] = el}
              video={video}
              isActive={index === currentVideoIndex}
              onReaction={onReaction}
              userId={userId}
            />
          </div>
        ))}
      </div>

      {/* Навигационные кнопки */}
      <div className="navigation-controls">
        {currentVideoIndex > 0 && (
          <button 
            className="nav-button nav-previous"
            onClick={handlePrevious}
            aria-label="Предыдущее видео"
          >
            ↑
          </button>
        )}
        
        {currentVideoIndex < videos.length - 1 && (
          <button 
            className="nav-button nav-next"
            onClick={handleNext}
            aria-label="Следующее видео"
          >
            ↓
          </button>
        )}
      </div>

      {/* Индикатор позиции */}
      <div className="position-indicator">
        {currentVideoIndex + 1} / {videos.length}
      </div>
    </div>
  )
}

export default VideoFeed 