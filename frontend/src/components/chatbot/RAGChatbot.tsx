// src/components/chatbot/RAGChatbot.tsx
import React, { useState, useEffect } from 'react';
import ChatBox from './ChatBox';

interface RAGChatbotProps {
  /**
   * Optional container selector where text selection should be detected
   * If not provided, will listen for selections on the entire document
   */
  containerSelector?: string;
}

const RAGChatbot: React.FC<RAGChatbotProps> = ({ containerSelector }) => {
  const [selectedText, setSelectedText] = useState<string>('');

  useEffect(() => {
    const handleSelection = () => {
      const selectedTextContent = window.getSelection()?.toString().trim();

      if (selectedTextContent) {
        // Only update if the selected text is substantial (more than 5 characters)
        if (selectedTextContent.length > 5) {
          setSelectedText(selectedTextContent);
        }
      }
    };

    // Add event listeners for text selection
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    // If a specific container is provided, also listen for selections within that container
    let containerElement: HTMLElement | null = null;
    if (containerSelector) {
      containerElement = document.querySelector(containerSelector);
      if (containerElement) {
        containerElement.addEventListener('mouseup', handleSelection);
        containerElement.addEventListener('keyup', handleSelection);
      }
    }

    // Cleanup event listeners on unmount
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);

      if (containerElement) {
        containerElement.removeEventListener('mouseup', handleSelection);
        containerElement.removeEventListener('keyup', handleSelection);
      }
    };
  }, [containerSelector]);

  const clearSelectedText = () => {
    setSelectedText('');
    // Clear the current selection in the browser
    window.getSelection()?.empty();
  };

  return (
    <div className="rag-chatbot-container">
      {selectedText && (
        <div className="mb-3 p-2 bg-blue-50 border border-blue-200 rounded text-sm">
          <div className="flex justify-between items-start">
            <div>
              <span className="font-medium text-blue-800">Selected Text:</span>
              <p className="mt-1 text-blue-700 italic">"{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"</p>
            </div>
            <button
              onClick={clearSelectedText}
              className="text-blue-700 hover:text-blue-900 font-medium ml-2"
            >
              Clear
            </button>
          </div>
        </div>
      )}
      <ChatBox selectedText={selectedText} />
    </div>
  );
};

export default RAGChatbot;