import React from 'react';
import DocPage from '@theme-original/DocPage';
import RAGChatbot from '@site/src/components/RAGChatbot';

// Wrapper for DocPage that includes the RAG Chatbot
export default function DocPageWrapper(props) {
  return (
    <>
      <DocPage {...props} />
      <RAGChatbot />
    </>
  );
}