# 🤖 AI Agent Engineering Template

**Ready-to-use template for building AI agents and applications.** Choose your stack and start building immediately!

> 🚀 **Quick Start**: Click "Use this template" above to create your new AI project!

## 🎯 Choose Your Stack

### 🚀 TypeScript + Next.js (`ts-bootcamp-project/`)
- **Framework**: Next.js 14 with App Router
- **AI Integration**: Vercel AI SDK with OpenAI
- **UI**: Shadcn UI + Tailwind CSS
- **Perfect for**: Web apps, chatbots, user-facing agents

### 🐍 Python + LiteLLM (`python-bootcamp-project/`)
- **Package Manager**: uv (fast & modern)
- **AI Integration**: LiteLLM (100+ LLM providers)
- **Perfect for**: Scripts, APIs, data processing, backend agents

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

## 🛠️ Setup Instructions

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.8 or higher)
- OpenAI API key

### TypeScript/Next.js Setup

1. Navigate to the TypeScript project:
   ```bash
   cd ts-bootcamp-project
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Create `.env.local` file:
   ```bash
   OPENAI_API_KEY=your-actual-api-key-here
   ```

4. Run the development server:
   ```bash
   pnpm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

### Python Setup

1. Navigate to the Python project:
   ```bash
   cd python-bootcamp-project
   ```

2. Create `.env` file:
   ```bash
   OPENAI_API_KEY=your-actual-api-key-here
   ```

3. Run the Python script:
   ```bash
   uv run python main.py
   ```

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
