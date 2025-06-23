# 🤖 Agent Engineering Bootcamp - YouTube Channel Agent

**Week 2 Homework Submission: Two-Tool Agent Implementation**

> 🎯 **Main Project**: [`python-bootcamp-project/`](./python-bootcamp-project/) - YouTube Channel Agent MVP
> 
> 📝 **Assignment**: Build an agent with two tools 

## 🏆 Homework Submission: YouTube Channel Agent

### 📍 **Primary Focus**: `python-bootcamp-project/`

**Two-Tool Architecture:**
1. **🔍 YouTube Content Crawler** - Discovers and extracts content from YouTube channels
2. **🧠 RAG Knowledge Assistant** - Provides intelligent Q&A using retrieved video content

**Key Features:**
- ✅ Semantic search across video transcripts
- ✅ History-aware conversation memory  
- ✅ Source attribution with video links
- ✅ Interactive Streamlit web interface
- ✅ Pre-built MCP development knowledge base

**[📖 Full Documentation →](./python-bootcamp-project/README.md)**

---

## 🎯 Repository Structure

### 🐍 **Python Project** (Main Submission)
**Location**: `python-bootcamp-project/`
- **Purpose**: Week 2 homework - Two-tool agent system
- **Status**: ✅ Complete with comprehensive documentation
- **Tech Stack**: Python, Streamlit, LangChain, ChromaDB, OpenAI
- **Features**: YouTube content analysis + RAG Q&A system

### 🚀 **TypeScript Project** (Template)
**Location**: `ts-bootcamp-project/`
- **Purpose**: Template for future TypeScript projects
- **Status**: 🚧 Template/boilerplate code
- **Tech Stack**: Next.js, Vercel AI SDK, Shadcn UI

## 📋 Template Usage

### 1. Create New Project
1. Click **"Use this template"** (green button above)
2. Name your project (e.g., `my-ai-chatbot`)
3. Clone your new repository locally

### 2. Choose Your Stack
```bash
# Keep only the stack you need
rm -rf python-bootcamp-project/  # If using TypeScript
# OR
rm -rf ts-bootcamp-project/      # If using Python
```

## 🛠️ Quick Start (Python Project)

### Prerequisites
- Python 3.12+
- OpenAI API key
- YouTube Data API v3 key

### Setup & Run
```bash
# Navigate to main project
cd python-bootcamp-project

# Install dependencies  
uv sync

# Configure credentials
cp credentials.yml.example credentials.yml
# Add your API keys to credentials.yml

# Run the application
uv run streamlit run youtube_agent_mvp.py
```

**[📖 Detailed Setup Instructions →](./python-bootcamp-project/README.md)**

### TypeScript Project (Template Only)
The `ts-bootcamp-project/` contains template code for future projects. See the project README for setup instructions if needed.

## 🔑 API Key Setup

1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Create an API key at [API Keys page](https://platform.openai.com/api-keys)
3. Add the key to both `.env.local` (TypeScript) and `.env` (Python) files
4. **Important**: Never commit your API keys to version control!

## 📚 Technologies Used

### TypeScript Stack
- **Next.js 14**: React framework with App Router
- **AI SDK**: Vercel's AI SDK for streaming AI responses
- **Shadcn UI**: Modern UI component library
- **Tailwind CSS**: Utility-first CSS framework
- **TypeScript**: Type-safe JavaScript

### Python Stack
- **uv**: Fast Python package manager
- **LiteLLM**: Unified LLM interface
- **python-dotenv**: Environment variable management
- **OpenAI**: Direct OpenAI API integration

## 🎯 Features

### TypeScript App Features
- ✨ AI-powered poem generation
- 🔄 Real-time streaming responses
- 🎨 Beautiful UI with dark/light mode
- 📱 Responsive design
- 🔄 Regenerate and hide poem functionality

### Python App Features
- 🤖 Simple AI chat interface
- 🔗 LiteLLM for multiple AI provider support
- 🔧 Easy configuration and setup
- 📝 Clean, readable code structure

## 🚀 Deployment

### TypeScript (Vercel)
1. Connect your GitHub repo to Vercel
2. Add `OPENAI_API_KEY` to Vercel environment variables
3. Deploy automatically on push to main branch

### Python (Multiple Options)
- **Heroku**: Add Procfile and requirements.txt
- **Railway**: Direct deployment from GitHub
- **AWS Lambda**: Serverless deployment
- **Google Cloud**: Cloud Run deployment

## 📖 Learning Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Vercel AI SDK](https://sdk.vercel.ai/)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

## 🤝 Contributing

This is a personal learning repository for the Break Into Data: AI Agent Engineering Bootcamp, [https://breakintodata.io/](https://breakintodata.io/). Feel free to fork and experiment with your own implementations!

## 📄 License

This project is for educational purposes as part of the Agent Engineering Bootcamp.

---

**Happy Coding!** 🎉 Built with ❤️ for the Break Into Data: AI Agent Engineering Bootcamp, [https://breakintodata.io/](https://breakintodata.io/)
