import React, { useState } from 'react';
import ChatBox from '../components/ChatBox';

const Dashboard: React.FC = () => {
  const [selectedText, setSelectedText] = useState<string>('');

  // Function to handle text selection
  const handleTextSelection = () => {
    const selectedTextContent = window.getSelection()?.toString().trim();
    if (selectedTextContent) {
      setSelectedText(selectedTextContent);
    }
  };

  // Function to clear the selected text
  const clearSelectedText = () => {
    setSelectedText('');
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <header className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">AI_BOOK Dashboard</h1>
          <p className="text-gray-600">Ask questions about AI_BOOK content using our RAG system</p>
        </header>

        <main className="flex flex-col items-center">
          {selectedText && (
            <div className="w-full max-w-4xl mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <div className="flex justify-between items-start">
                <div>
                  <span className="font-semibold text-yellow-800">Selected Text:</span>
                  <p className="mt-1 text-yellow-700 italic">"{selectedText.substring(0, 150)}{selectedText.length > 150 ? '...' : ''}"</p>
                </div>
                <button
                  onClick={clearSelectedText}
                  className="text-yellow-700 hover:text-yellow-900 text-sm font-medium"
                >
                  Clear
                </button>
              </div>
            </div>
          )}

          <div className="w-full flex flex-col items-center">
            <div
              className="w-full max-w-4xl mb-6 p-6 bg-white rounded-lg shadow-md"
              onMouseUp={handleTextSelection}
            >
              <h2 className="text-xl font-bold mb-3 text-gray-800">Sample AI Book Content</h2>
              <p className="text-gray-700 mb-2">
                Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.
              </p>
              <p className="text-gray-700 mb-2">
                AI applications include advanced web search engines, recommendation systems, understanding human speech, mobile apps, self-driving cars, automated decision-making, and competing at the highest level in strategic game systems. As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect.
              </p>
              <p className="text-gray-700">
                Modern machine learning techniques are at the heart of AI. Problems for AI applications include reasoning, knowledge representation, planning, learning, natural language processing, perception, and the ability to move and manipulate objects. General intelligence is among the field's long-term goals.
              </p>
              <div className="mt-4 text-sm text-gray-500 italic">
                Select any text above to ask specific questions about it using the chat interface below.
              </div>
            </div>
            <ChatBox selectedText={selectedText} />
          </div>

          <div className="mt-8 text-center text-gray-600 max-w-2xl">
            <h2 className="text-xl font-semibold mb-2">How to use</h2>
            <ul className="list-disc list-inside text-left space-y-1">
              <li>Type your question in the input box and press Send to get a response</li>
              <li>Select text on this page and then ask questions about it</li>
              <li>Use the Clear button to reset the conversation</li>
            </ul>
          </div>
        </main>

        <footer className="mt-12 text-center text-gray-500 text-sm">
          <p>Powered by AI_BOOK RAG System • Backend running on http://127.0.0.1:8000</p>
        </footer>
      </div>
    </div>
  );
};

export default Dashboard;