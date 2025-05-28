// API базовый URL - в production это будет настроено через переменные окружения
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api'

class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

const handleResponse = async (response) => {
  if (!response.ok) {
    const errorText = await response.text()
    throw new ApiError(`HTTP ${response.status}: ${errorText}`, response.status)
  }
  
  const contentType = response.headers.get('content-type')
  if (contentType && contentType.includes('application/json')) {
    return await response.json()
  }
  
  return await response.text()
}

export const fetchVideoFeed = async (chatId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/feed?chat_id=${chatId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    return await handleResponse(response)
  } catch (error) {
    console.error('Error fetching video feed:', error)
    throw error
  }
}

export const sendReaction = async (userId, fileId, type) => {
  try {
    const response = await fetch(`${API_BASE_URL}/react`, {
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
    
    return await handleResponse(response)
  } catch (error) {
    console.error('Error sending reaction:', error)
    throw error
  }
}

export const fetchVideoInfo = async (fileId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/video/${fileId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    return await handleResponse(response)
  } catch (error) {
    console.error('Error fetching video info:', error)
    throw error
  }
}

export const fetchStats = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/stats`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    return await handleResponse(response)
  } catch (error) {
    console.error('Error fetching stats:', error)
    throw error
  }
}

export const healthCheck = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    return await handleResponse(response)
  } catch (error) {
    console.error('Error checking health:', error)
    throw error
  }
} 