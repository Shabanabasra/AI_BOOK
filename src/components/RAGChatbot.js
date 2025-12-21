import React, { useState, useEffect } from 'react';
import ReactDom from 'react-dom';

// Define TypeScript-like interfaces using PropTypes
const { useState, useEffect } = React;

// API service for backend communication
const apiService = {
  async sendChatMessage(question) {
    try {
      const backendUrl = process.env.REACT_APP_API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${backendUrl}/api/v1/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending chat message:', error);
      throw error;
    }
  },

  async askFromSelection(selectedText, question) {
    try {
      const backendUrl = process.env.REACT_APP_API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${backendUrl}/api/v1/ask-from-selection`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          selected_text: selectedText,
          question,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error asking from selection:', error);
      throw error;
    }
  }
};

// Message type
const Message = ({ message }) => {
  return (
    <div className={`message ${message.sender}`} style={{
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
};

// ChatBox component
const ChatBox = ({ selectedText = null }) => {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      let response;
      if (selectedText) {
        response = await apiService.askFromSelection(selectedText, inputValue);
      } else {
        response = await apiService.sendChatMessage(inputValue);
      }

      const botMessage = {
        id: `bot-${Date.now()}`,
        text: response.answer || response.query || 'No response received',
        sender: 'bot',
        timestamp: new Date(),
        references: response.references || [],
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error('Error getting response:', err);
      setError('Failed to get response from the AI. Please try again.');

      const errorMessage = {
        id: `error-${Date.now()}`,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{
      border: '1px solid #ddd',
      borderRadius: '8px',
      padding: '16px',
      backgroundColor: 'white',
      maxHeight: '400px',
      display: 'flex',
      flexDirection: 'column'
    }}>
      <div style={{ flex: 1, overflowY: 'auto', marginBottom: '12px' }}>
        {messages.length === 0 ? (
          <div style={{ textAlign: 'center', color: '#666', fontStyle: 'italic' }}>
            {selectedText
              ? 'Ask a question about the selected text...'
              : 'Ask a question about the AI book content...'}
          </div>
        ) : (
          messages.map(message => (
            <Message key={message.id} message={message} />
          ))
        )}
        {isLoading && (
          <div style={{ display: 'flex', justifyContent: 'flex-start', marginBottom: '10px' }}>
            <div style={{ backgroundColor: '#e9ecef', padding: '8px 12px', borderRadius: '8px' }}>
              <div style={{ display: 'flex', gap: '4px' }}>
                <div style={{ width: '8px', height: '8px', backgroundColor: '#666', borderRadius: '50%', animation: 'bounce 1s infinite' }}>•</div>
                <div style={{ width: '8px', height: '8px', backgroundColor: '#666', borderRadius: '50%', animation: 'bounce 1s infinite 0.2s' }}>•</div>
                <div style={{ width: '8px', height: '8px', backgroundColor: '#666', borderRadius: '50%', animation: 'bounce 1s infinite 0.4s' }}>•</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div style={{ color: 'red', fontSize: '0.9em', marginBottom: '8px' }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '8px' }}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={selectedText ? "Ask about selected text..." : "Ask about the content..."}
          style={{
            flex: 1,
            padding: '8px',
            border: '1px solid #ccc',
            borderRadius: '4px'
          }}
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          style={{
            padding: '8px 16px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: !inputValue.trim() || isLoading ? 'not-allowed' : 'pointer',
            opacity: !inputValue.trim() || isLoading ? 0.6 : 1
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
};

// Main RAG Chatbot Component
const RAGChatbot = () => {
  const [selectedText, setSelectedText] = useState('');
  const [showChat, setShowChat] = useState(false);

  useEffect(() => {
    const handleSelection = () => {
      const selectedTextContent = window.getSelection?.()?.toString()?.trim() || '';

      if (selectedTextContent && selectedTextContent.length > 5) {
        setSelectedText(selectedTextContent);
        setShowChat(true);
      } else {
        setSelectedText('');
        if (!selectedTextContent) {
          setShowChat(false);
        }
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, []);

  const clearSelection = () => {
    setSelectedText('');
    setShowChat(false);
    if (window.getSelection) {
      window.getSelection().removeAllRanges();
    }
  };

  return (
    <div style={{ position: 'relative' }}>
      {showChat && selectedText && (
        <div style={{
          position: 'fixed',
          top: '20px',
          right: '20px',
          zIndex: '1000',
          width: '350px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          borderRadius: '8px',
          backgroundColor: 'white'
        }}>
          <div style={{
            padding: '12px',
            backgroundColor: '#f8f9fa',
            borderBottom: '1px solid #dee2e6',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <strong>AI Assistant</strong>
            <button
              onClick={clearSelection}
              style={{
                background: 'none',
                border: 'none',
                fontSize: '1.2em',
                cursor: 'pointer',
                color: '#666'
              }}
            >
              ×
            </button>
          </div>
          <div style={{ padding: '12px' }}>
            <div style={{
              backgroundColor: '#e7f3ff',
              padding: '8px',
              borderRadius: '4px',
              marginBottom: '12px',
              fontSize: '0.9em'
            }}>
              <strong>Selected:</strong> "{selectedText.substring(0, 80)}{selectedText.length > 80 ? '...' : ''}"
            </div>
            <ChatBox selectedText={selectedText} />
          </div>
        </div>
      )}
    </div>
  );
};

export default RAGChatbot;