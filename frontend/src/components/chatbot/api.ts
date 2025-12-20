// src/components/chatbot/api.ts
import { ChatRequest, ChatResponse, AskFromSelectionRequest, AskFromSelectionResponse } from './types';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

/**
 * Function to send a general chat question to the backend
 */
export const sendChatMessage = async (question: string): Promise<ChatResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
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