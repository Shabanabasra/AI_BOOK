import React, { useState, useEffect, FormEvent } from 'react';

// Define message type
type MessageType = {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  references?: string[];
};

// API service for backend
const apiService = {
  async sendChatMessage(question: string) {
    try {
      const backendUrl = process.env.REACT_APP_API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${backendUrl}/api/v1/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Error sending chat message:', error);
      throw error;
    }
  },
};

// Single message component
const Message = ({ message }: { message: MessageType }) => (
  <div style={{
    display: 'flex',
    justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
    marginBottom: '10px'
  }}>
    <div style={{
      backgroundColor: message.sender === 'user' ? '#007bff' : '#e9ecef',
      color: message.sender === 'user' ? 'white' : 'black',
      padding: '8px 12px',
      borderRadius: '8px',
      maxWidth: '80%',
      wordWrap: 'break-word'
    }}>
      {message.text}
      {message.references && message.references.length > 0 && (
        <div style={{ fontSize: '0.8em', marginTop: '4px' }}>
          <strong>References:</strong> {message.references.join(', ')}
        </div>
      )}
    </div>
  </div>
);

// ChatBox component
const ChatBox = () => {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage: MessageType = { id: Date.now().toString(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await apiService.sendChatMessage(inputValue);
      const botMessage: MessageType = {
        id: `bot-${Date.now()}`,
        text: response.answer || 'No response received',
        sender: 'bot',
        references: response.references || [],
      };
      setMessages(prev => [...prev, botMessage]);
    } catch {
      setMessages(prev => [...prev, { id: `error-${Date.now()}`, text: 'Error fetching response', sender: 'bot' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '16px', maxHeight: '400px', display: 'flex', flexDirection: 'column' }}>
      <div style={{ flex: 1, overflowY: 'auto', marginBottom: '12px' }}>
        {messages.map(msg => <Message key={msg.id} message={msg} />)}
      </div>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '8px' }}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask about the content..."
          style={{ flex: 1, padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
        />
        <button type="submit" disabled={!inputValue.trim() || isLoading} style={{ padding: '8px 16px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}>
          Send
        </button>
      </form>
    </div>
  );
};

// Main RAGChatbot component
const RAGChatbot = () => <ChatBox />;

export default RAGChatbot;