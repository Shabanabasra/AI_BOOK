// src/components/chatbot/types.ts
export interface ChatRequest {
  question: string;
}

export interface ChatResponse {
  answer: string;
  references: string[];
}

export interface AskFromSelectionRequest {
  selected_text: string;
  question: string;
}

export interface AskFromSelectionResponse {
  answer: string;
  references: string[];
}

export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  references?: string[];
}