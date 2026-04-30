import React, { useState, useEffect } from 'react'
import Avatar from './components/Avatar'
import ChatInterface from './components/ChatInterface'
import './App.css'

function App() {
  const [agentInfo, setAgentInfo] = useState(null)
  const [conversationId, setConversationId] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch agent info on mount
    fetchAgentInfo()
  }, [])

  const fetchAgentInfo = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/chat/agent-info`)
      const data = await response.json()
      setAgentInfo(data)
    } catch (error) {
      console.error('Failed to fetch agent info:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Initializing agent...</div>
  }

  return (
    <div className="App">
      <div className="container">
        <div className="avatar-section">
          {agentInfo && <Avatar agentInfo={agentInfo} />}
        </div>
        <div className="chat-section">
          {agentInfo && (
            <ChatInterface
              agentInfo={agentInfo}
              conversationId={conversationId}
              onConversationIdChange={setConversationId}
            />
          )}
        </div>
      </div>
    </div>
  )
}

export default App
