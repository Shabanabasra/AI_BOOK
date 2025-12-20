// src/components/chatbot/ChatBox.tsx
import React, { useState, useEffect, useRef } from 'react';
import { Message } from './types';
import { sendChatMessage, askFromSelection } from './api';

interface ChatBoxProps {
  selectedText?: string;
}

const ChatBox: React.FC<ChatBoxProps> = ({ selectedText }) => {
  const [inputValue, setInputValue] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Scroll to bottom of messages when new messages are added
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      let response;
      if (selectedText) {
        // Use ask-from-selection endpoint if text is selected
        response = await askFromSelection(selectedText, inputValue);
      } else {
        // Use regular chat endpoint
        response = await sendChatMessage(inputValue);
      }

      const botMessage: Message = {
        id: `bot-${Date.now()}`,
        text: response.answer,
        sender: 'bot',
        timestamp: new Date(),
        references: response.references || [],
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error('Error getting response:', err);
      setError('Failed to get response from the AI. Please try again.');

      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setMessages([]);
    setError(null);
  };

  // Function to highlight references in text
  const highlightReferences = (text: string, references: string[] = []) => {
    let highlightedText = text;

    // Highlight AI_BOOK references
    highlightedText = highlightedText.replace(
      /(AI_BOOK)/gi,
      '<strong class="text-blue-600 font-bold">$1</strong>'
    );

    // Highlight references if they exist
    references.forEach(ref => {
      const regex = new RegExp(`(${ref})`, 'gi');
      highlightedText = highlightedText.replace(
        regex,
        '<strong class="text-green-600 font-bold">$1</strong>'
      );
    });

    return highlightedText;
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden border border-gray-200">
      {/* Chat Header */}
      <div className="bg-gray-800 text-white p-3">
        <h2 className="text-lg font-semibold">AI_BOOK Assistant</h2>
        {selectedText && (
          <div className="mt-1 text-xs bg-gray-700 p-1 rounded">
            <span className="font-medium">Context:</span> {selectedText.substring(0, 80)}...
          </div>
        )}
      </div>

      {/* Chat Messages Area */}
      <div className="flex-1 overflow-y-auto p-3 bg-gray-50" style={{ maxHeight: '400px' }}>
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500 text-center p-4">
            <p>Ask a question about the content or select text to ask specific questions</p>
          </div>
        ) : (
          <div className="space-y-3">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className="max-w-[85%]">
                  <div
                    className={`rounded-lg p-3 mb-1 ${
                      message.sender === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-200 text-gray-800'
                    }`}
                    dangerouslySetInnerHTML={{
                      __html: highlightReferences(message.text, message.references)
                    }}
                  />
                  {message.references && message.references.length > 0 && (
                    <div className="text-xs text-gray-600 mt-1">
                      <span className="font-medium">References:</span> {message.references.join(', ')}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-200 text-gray-800 rounded-lg p-3">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border-t border-red-400 text-red-700 px-3 py-2 text-sm">
          {error}
        </div>
      )}

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="border-t p-3 bg-white">
        <div className="flex">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={selectedText ? "Ask about selected text..." : "Ask a question about the content..."}
            className="flex-1 border border-gray-300 rounded-l-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-500 text-sm"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="bg-blue-600 text-white px-4 py-2 rounded-r-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
          >
            Send
          </button>
        </div>
        <div className="flex justify-between mt-2">
          <button
            type="button"
            onClick={handleClear}
            className="text-xs text-gray-600 hover:text-gray-800 underline"
          >
            Clear Chat
          </button>
          <div className="text-xs text-gray-500">
            {selectedText && <span className="text-blue-600">Context active</span>}
          </div>
        </div>
      </form>
    </div>
  );
};

export default ChatBox;