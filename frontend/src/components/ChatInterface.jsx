import React, { useState, useRef, useEffect } from 'react'
import './ChatInterface.css'
import VoiceInput from './VoiceInput'

function ChatInterface({ agentInfo, conversationId, onConversationIdChange }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const messagesEndRef = useRef(null)
  const audioRef = useRef(null)

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    // Add user message
    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/chat/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_message: input,
          conversation_id: conversationId,
          include_tts: true
        })
      })

      if (!response.ok) throw new Error('Failed to get response')

      const data = await response.json()
      onConversationIdChange(data.conversation_id)

      // Add assistant message
      const assistantMessage = { role: 'assistant', content: data.assistant_message }
      setMessages(prev => [...prev, assistantMessage])

      // Play audio if available
      if (data.audio_base64) {
        playAudio(data.audio_base64)
      }
    } catch (error) {
      console.error('Error:', error)
      const errorMessage = { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const playAudio = (audioBase64) => {
    const audioBlob = base64ToBlob(audioBase64, 'audio/mp3')
    const audioUrl = URL.createObjectURL(audioBlob)
    if (audioRef.current) {
      audioRef.current.src = audioUrl
      setIsPlaying(true)
      audioRef.current.play()
    }
  }

  const base64ToBlob = (base64, type) => {
    const binary = atob(base64)
    const array = new Uint8Array(binary.length)
    for (let i = 0; i < binary.length; i++) {
      array[i] = binary.charCodeAt(i)
    }
    return new Blob([array], { type })
  }

  const handleVoiceInput = (transcript) => {
    setInput(transcript)
  }

  return (
    <div className="chat-interface">
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h3>Welcome to {agentInfo?.name}</h3>
            <p>Start a conversation by typing a message or using voice input</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-content">{msg.content}</div>
            </div>
          ))
        )}
        {loading && (
          <div className="message assistant">
            <div className="typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <form onSubmit={sendMessage}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={loading}
          />
          <button type="submit" disabled={loading || !input.trim()}>
            Send
          </button>
        </form>
        <VoiceInput onTranscript={handleVoiceInput} />
      </div>

      <audio ref={audioRef} onEnded={() => setIsPlaying(false)} />
    </div>
  )
}

export default ChatInterface
