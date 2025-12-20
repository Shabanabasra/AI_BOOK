import { ChatRequest, ChatResponse, AskFromSelectionRequest, AskFromSelectionResponse, RetrievedDocument } from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Define the response type for the new CCR-compliant chat endpoint
interface CCRChatResponse {
  query: string;
  retrieved_documents: RetrievedDocument[];
}

/**
 * Function to send a chat question to the backend (CCR-compliant version)
 */
export const sendChatMessage = async (question: string): Promise<ChatResponse> => {
  try {
    // Use the new CCR-compliant endpoint at the root level
    const response = await fetch('http://127.0.0.1:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: CCRChatResponse = await response.json();

    // Transform the CCR-compliant response to match the expected ChatResponse format
    // For now, we'll return a simple answer based on the retrieved documents
    const answer = data.retrieved_documents.length > 0
      ? `I found ${data.retrieved_documents.length} relevant documents. Here's what I can tell you based on the retrieved information:\n\n${data.retrieved_documents[0].content.substring(0, 500)}...`
      : "I couldn't find any relevant documents for your question.";

    return {
      answer,
      references: data.retrieved_documents.map(doc => `${doc.title} (${doc.score.toFixed(2)})`)
    };
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

/**
 * Function to send a chat question and get the raw retrieved documents (for enhanced display)
 */
export const sendChatMessageWithDocuments = async (question: string) => {
  try {
    // Use the new CCR-compliant endpoint at the root level
    const response = await fetch('http://127.0.0.1:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: CCRChatResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

/**
 * Function to send a selected text question to the backend
 */
export const askFromSelection = async (
  selectedText: string,
  question: string
): Promise<AskFromSelectionResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/ask-from-selection`, {
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

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error asking from selection:', error);
    throw error;
  }
};