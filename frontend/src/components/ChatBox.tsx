import React, { useState, useRef, useEffect } from 'react';
import { Message, RetrievedDocument } from '../types';
import { sendChatMessage, askFromSelection, sendChatMessageWithDocuments } from '../services/api';

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
      let retrievedDocs: RetrievedDocument[] = [];

      if (selectedText) {
        // Use ask-from-selection endpoint if text is selected
        response = await askFromSelection(selectedText, inputValue);
      } else {
        // Use the new CCR-compliant chat endpoint to get raw documents
        const ccrResponse = await sendChatMessageWithDocuments(inputValue);

        // Transform to match expected format
        response = {
          answer: ccrResponse.retrieved_documents.length > 0
            ? `I found ${ccrResponse.retrieved_documents.length} relevant documents. Here's what I can tell you based on the retrieved information:\n\n${ccrResponse.retrieved_documents[0].content.substring(0, 500)}...`
            : "I couldn't find any relevant documents for your question.",
          references: ccrResponse.retrieved_documents.map((doc: RetrievedDocument) => `${doc.title} (${doc.score.toFixed(2)})`)
        };

        retrievedDocs = ccrResponse.retrieved_documents;
      }

      const botMessage: Message = {
        id: `bot-${Date.now()}`,
        text: response.answer,
        sender: 'bot',
        timestamp: new Date(),
        references: response.references || [],
        retrievedDocuments: retrievedDocs
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

  // Function to highlight AI_BOOK references in text
  const highlightAIBook = (text: string) => {
    return text.replace(/(AI_BOOK)/gi, '<strong class="text-blue-600 font-bold">$1</strong>');
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Chat Header */}
      <div className="bg-gray-800 text-white p-4">
        <h1 className="text-xl font-bold">AI_BOOK RAG Chatbot</h1>
        {selectedText && (
          <div className="mt-2 text-sm bg-gray-700 p-2 rounded">
            <span className="font-semibold">Selected Text:</span> {selectedText.substring(0, 100)}...
          </div>
        )}
      </div>

      {/* Chat Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50" style={{ maxHeight: '500px' }}>
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            <p>Start a conversation by typing a message below...</p>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className="max-w-[80%]">
                  <div
                    className={`rounded-lg p-3 mb-1 ${
                      message.sender === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-200 text-gray-800'
                    }`}
                    dangerouslySetInnerHTML={{
                      __html: highlightAIBook(message.text)
                    }}
                  />
                  {message.references && message.references.length > 0 && (
                    <div className="text-xs text-gray-500 mt-1">
                      <span className="font-semibold">References:</span> {message.references.join(', ')}
                    </div>
                  )}
                  {/* Display retrieved documents if available */}
                  {message.retrievedDocuments && message.retrievedDocuments.length > 0 && (
                    <div className="mt-2 border-t border-gray-300 pt-2">
                      <div className="text-xs font-semibold text-gray-700 mb-1">Retrieved Documents:</div>
                      {message.retrievedDocuments.slice(0, 3).map((doc, index) => (
                        <div key={index} className="text-xs bg-white border border-gray-200 rounded p-2 mb-1">
                          <div className="font-medium text-blue-700">{doc.title}</div>
                          <div className="text-gray-600 truncate" title={doc.content}>{doc.content.substring(0, 100)}{doc.content.length > 100 ? '...' : ''}</div>
                          <div className="text-gray-500">Score: {doc.score.toFixed(3)} | Source: {doc.source}</div>
                        </div>
                      ))}
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
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 text-sm">
          {error}
        </div>
      )}

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="border-t p-4 bg-white">
        <div className="flex">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your question here..."
            className="flex-1 border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
        <div className="flex mt-2 space-x-2">
          <button
            type="button"
            onClick={handleClear}
            className="text-sm text-gray-600 hover:text-gray-800 underline"
          >
            Clear Chat
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatBox;