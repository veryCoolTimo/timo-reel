const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
  async getFeed(chatId) {
    const response = await fetch(`${API_BASE_URL}/feed?chat_id=${chatId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch feed');
    }
    return response.json();
  },

  async sendReaction(userId, fileId, type) {
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
    });
    
    if (!response.ok) {
      throw new Error('Failed to send reaction');
    }
    
    return response.json();
  }
}; 