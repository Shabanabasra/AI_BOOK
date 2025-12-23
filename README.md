# AI BOOK - Physical AI & Humanoid Robotics Textbook

A comprehensive textbook and learning platform covering Physical AI and Humanoid Robotics, built with Docusaurus and powered by a FastAPI RAG backend.

## 📚 Overview

AI BOOK is a complete educational resource that covers:

1. **Introduction to Physical AI** - Understanding AI systems that interact with the physical world
2. **Basics of Humanoid Robotics** - Creating robots that mimic human movements and behaviors
3. **ROS 2 Fundamentals** - Robot Operating System for building robot applications
4. **Digital Twin Simulation** - Virtual models of physical systems
5. **Vision-Language-Action Systems** - AI systems that perceive, understand, and act
6. **Capstone: AI to Robot** - Connecting AI systems to physical robots

Each chapter includes:
- Simple concepts explained clearly
- ASCII diagrams for visualization
- Hands-on exercises
- Mini glossary
- Short quizzes
- Real-world examples
- Optional Urdu explanations

## 🏗️ Architecture

The project consists of two main components:

### Frontend (Docusaurus)
- Static textbook website
- Auto-generated sidebar
- Responsive design
- Built with Docusaurus v3
- Deployable to GitHub Pages or Vercel

### Backend (FastAPI)
- RAG (Retrieval Augmented Generation) API
- Qdrant vector database for semantic search
- Sentence Transformers for embeddings
- Pre-loaded with AI BOOK content
- RESTful API endpoints

## 🚀 Quick Start

### Frontend Setup
```bash
cd frontend
npm install
npm start  # For development
npm run build  # To build for production
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Prerequisites for Backend
- Python 3.8+
- Qdrant vector database (can run locally or use cloud service)

## 📁 Project Structure

```
AI_BOOK/
├── frontend/           # Docusaurus textbook site
│   ├── docs/           # AI BOOK content
│   │   └── AI_BOOK/    # 6 textbook chapters
│   ├── src/            # Custom components and CSS
│   ├── docusaurus.config.js  # Site configuration
│   └── sidebars.js     # Auto-generated sidebar
├── backend/            # FastAPI RAG service
│   ├── app/            # Main application
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile      # Container configuration
└── README.md
```

## 🎯 Features

- **Beginner-friendly**: Concepts explained simply with clear examples
- **Interactive**: Hands-on exercises in each chapter
- **Visual**: ASCII diagrams to illustrate concepts
- **Multilingual**: Optional Urdu explanations
- **Self-testing**: Quizzes to reinforce learning
- **Real-world**: Practical examples from industry
- **Searchable**: Backend RAG API for content queries
- **Responsive**: Works on all device sizes

## 🛠️ Technologies Used

- **Frontend**: Docusaurus v3, React, TypeScript
- **Backend**: FastAPI, Python, Qdrant, Sentence Transformers
- **Deployment**: Vercel (frontend), Docker (backend)
- **Documentation**: Markdown, MDX

## 🚀 Deployment

### Frontend (Vercel)
The frontend is configured for Vercel deployment:
1. Connect your GitHub repository to Vercel
2. Set build command to `npm run build`
3. Set output directory to `build`

### Backend (Self-hosted)
Deploy the backend using Docker:
```bash
docker build -t ai-book-backend .
docker run -p 8000:8000 ai-book-backend
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎓 Learning Path

1. Start with Chapter 1: Introduction to Physical AI
2. Progress through each chapter sequentially
3. Complete hands-on exercises in each chapter
4. Use the backend API to search and explore content
5. Complete the capstone project in Chapter 6

## 📞 Support

For support, please open an issue in the GitHub repository.

---

Built with ❤️ for the AI and Robotics community.
