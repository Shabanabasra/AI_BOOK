# AI_BOOK RAG Chatbot Dashboard

This is the frontend dashboard for the AI_BOOK RAG Chatbot system. It provides a user-friendly interface to interact with the AI_BOOK backend.

## Features

- Chat interface for asking questions about AI_BOOK content
- Support for asking questions about selected text
- Loading indicators during AI processing
- Error handling for backend connection issues
- Clean, responsive UI with Tailwind CSS

## Prerequisites

- Node.js (v16 or higher)
- The backend server running at http://127.0.0.1:8000

## Getting Started

1. Make sure the backend server is running:
   ```bash
   cd backend
   python main.py
   ```

2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to http://localhost:3000

## Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the project for production
- `npm run serve` - Preview the production build

## Project Structure

```
frontend/
├── src/
│   ├── components/     # React components
│   │   └── ChatBox.tsx # Main chat interface
│   ├── pages/          # Page components
│   │   └── dashboard.tsx # Dashboard page
│   ├── services/       # API service functions
│   │   └── api.ts      # Backend API calls
│   ├── types.ts        # TypeScript type definitions
│   ├── App.tsx         # Main App component
│   └── index.tsx       # Entry point
├── public/             # Static assets
├── package.json        # Dependencies and scripts
├── vite.config.ts      # Vite configuration
├── tailwind.config.js  # Tailwind CSS configuration
└── tsconfig.json       # TypeScript configuration
```

## Backend Integration

The frontend connects to the backend at `http://127.0.0.1:8000` and uses these endpoints:

- `POST /api/v1/chat` - For general questions
- `POST /api/v1/ask-from-selection` - For questions about selected text

## License

This project is part of the AI_BOOK system.