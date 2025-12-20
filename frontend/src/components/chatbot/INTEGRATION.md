# Docusaurus RAG Chatbot Integration Guide

## Overview
This guide explains how to integrate the RAG chatbot into your Docusaurus site. The chatbot allows users to ask questions about the book content and select text for context-specific questions.

## Installation

### 1. Copy the Chatbot Components
Copy all files from the `src/components/chatbot/` directory to your Docusaurus project:
- `src/components/chatbot/ChatBox.tsx`
- `src/components/chatbot/RAGChatbot.tsx`
- `src/components/chatbot/api.ts`
- `src/components/chatbot/types.ts`

### 2. Update Dependencies
Make sure your Docusaurus project has the required dependencies in `package.json`:

```json
{
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
```

### 3. Install Dependencies
```bash
npm install
```

## Integration Steps

### Method 1: Add to Specific Pages
To add the chatbot to a specific MDX page, import and use the `RAGChatbot` component:

```jsx
import RAGChatbot from '@site/src/components/chatbot/RAGChatbot';

<RAGChatbot containerSelector=".markdown" />
```

### Method 2: Add to All Pages (Layout Component)
To add the chatbot to all pages, modify your layout component in `src/theme/Layout/index.js`:

```jsx
import React from 'react';
import Layout from '@theme-original/Layout';
import RAGChatbot from '@site/src/components/chatbot/RAGChatbot';

export default function LayoutWrapper(props) {
  return (
    <Layout {...props}>
      {props.children}
      <div style={{ marginTop: '2rem' }}>
        <RAGChatbot containerSelector=".markdown" />
      </div>
    </Layout>
  );
}
```

### Method 3: As a Standalone Page
Create a standalone page at `src/pages/chat.mdx`:

```md
---
title: AI Assistant
---

import RAGChatbot from '@site/src/components/chatbot/RAGChatbot';

# AI Book Assistant

Ask questions about the content or select text to ask specific questions.

<RAGChatbot />
```

## Configuration Options

The `RAGChatbot` component accepts the following props:

- `containerSelector` (optional): CSS selector for the element where text selection should be detected (e.g., ".markdown" for Docusaurus content areas)

## Backend Connection

The chatbot connects to the backend API at `http://127.0.0.1:8000/api/v1` by default. The component handles:

- `/chat` endpoint for general questions
- `/ask-from-selection` endpoint for questions about selected text
- Error handling when the backend is unreachable
- Loading states during API requests

## Deployment Considerations

### For Production Deployment:
1. The backend server needs to be accessible from the deployed site
2. If the backend is only available locally, you may need to:
   - Deploy the backend to a public server
   - Use a proxy to forward requests
   - Implement a fallback mechanism for when the backend is unavailable

### Handling Backend Unavailability:
The component gracefully handles errors when the backend is unreachable by showing error messages to users.

## Customization

### Styling
The component uses Tailwind CSS classes that are compatible with Docusaurus themes. You can customize the appearance by:

1. Modifying the Tailwind classes in the component files
2. Adding custom CSS to your Docusaurus site

### Positioning
Adjust the chatbot's position by modifying the container where you place the component:

```jsx
<div style={{
  position: 'fixed',
  bottom: '20px',
  right: '20px',
  width: '400px',
  zIndex: 1000
}}>
  <RAGChatbot />
</div>
```

## Example Integration in Docusaurus Page

Here's a complete example of how to integrate the chatbot into a Docusaurus MDX page:

```mdx
---
title: Introduction to Physical AI
---

import RAGChatbot from '@site/src/components/chatbot/RAGChatbot';

# Introduction to Physical AI

Physical AI represents a significant advancement in artificial intelligence research, combining traditional AI approaches with physical world understanding...

## Key Concepts

- Embodied cognition
- Sensorimotor learning
- Physics-aware reasoning

{/* Add the chatbot below the content */}
<RAGChatbot containerSelector=".markdown" />

```

## Troubleshooting

### Common Issues:

1. **Text Selection Not Working**: Make sure the `containerSelector` prop matches the actual content area selector in your Docusaurus theme.

2. **Backend Connection Errors**: Verify that the backend server is running and accessible from the client browser.

3. **Styling Issues**: If the component doesn't match your theme, you may need to adjust the Tailwind classes or add custom CSS.

## Backend Requirements

Ensure your backend server is running at `http://127.0.0.1:8000` with the following endpoints available:

- `POST /api/v1/chat`
- `POST /api/v1/ask-from-selection`

The backend should accept JSON requests with the format:
- General questions: `{ "question": "Your question here" }`
- Selected text questions: `{ "selected_text": "Selected text", "question": "Your question about the text" }`

The backend should return responses in the format:
- `{ "answer": "Response text", "references": ["Reference 1", "Reference 2"] }`