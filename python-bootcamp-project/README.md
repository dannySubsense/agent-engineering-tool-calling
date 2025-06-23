# YouTube Channel Agent MVP

**Agent Engineering Bootcamp Week 2 - Two-Tool Agent Project**

## Overview

This project implements a YouTube Channel Agent that combines two powerful tools to create an intelligent knowledge base from YouTube content and provide conversational Q&A capabilities.

## 🛠️ Two-Tool Architecture

### Tool 1: YouTube Content Crawler
- **Purpose**: Discover and extract content from YouTube channels
- **Capabilities**: 
  - YouTube API search for videos by topic
  - Automatic transcript extraction using `pytubefix`
  - Metadata processing (title, channel, duration, view count)
  - CSV export functionality
- **Implementation**: Built with YouTube Data API v3 and transcript extraction

### Tool 2: RAG Knowledge Assistant  
- **Purpose**: Provide intelligent Q&A using retrieved video content
- **Capabilities**:
  - Vector similarity search with ChromaDB
  - History-aware conversation memory
  - Context-aware response generation
  - Source attribution with links to original videos
- **Implementation**: Advanced RAG system using LangChain, OpenAI embeddings, and Streamlit

## 🚀 Features

- **Database Management**: Choose existing knowledge bases or create new ones
- **Smart Search**: Semantic search across video transcripts
- **Conversational Memory**: Maintains context across chat sessions
- **Source Attribution**: Every response includes links to source videos
- **Interactive UI**: Clean Streamlit interface with quick questions
- **Real-time Processing**: Live video discovery and processing

## 📊 Current Knowledge Base

The system includes a pre-built knowledge base on **MCP (Model Context Protocol) Development** with 6 tutorial videos from Vibe Coding:

1. "Build An MCP Server In 5 Prompts"
2. "Let's Vibe Code an MCP Server in 10 Minutes" 
3. "Let's Vibe Code any API into our MCP server"
4. "The 'vibe coding' mind virus explained"
5. "Vibe Coding an MCP Server (As a Complete Beginner)"
6. "Here Is How to Vibe Code Large Scale Projects"

## 🔧 Technical Stack

- **Python 3.12** with UV package manager
- **Streamlit** for web interface
- **LangChain** for RAG implementation
- **ChromaDB** for vector storage
- **OpenAI** for embeddings and chat completion
- **YouTube Data API v3** for video discovery
- **pytubefix** for transcript extraction

## 📁 Project Structure

```
python-bootcamp-project/
├── main.py                    # Entry point
├── youtube_agent_mvp.py       # Main application
├── working_youtube_agent.py   # Alternative working version
├── credentials.yml            # API credentials
├── data/                      # Vector databases
├── documents/                 # Documentation
├── src/                       # Source code modules
├── tests/                     # Test files
├── pyproject.toml            # Dependencies
└── README.md                 # This file
```

## 🚦 Getting Started

### Prerequisites
- Python 3.12+
- UV package manager
- OpenAI API key
- YouTube Data API v3 key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python-bootcamp-project
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up credentials**
   - Copy `credentials.yml.example` to `credentials.yml`
   - Add your OpenAI and YouTube API keys

4. **Run the application**
   ```bash
   uv run streamlit run youtube_agent_mvp.py
   ```

## 💬 Usage

### Using Existing Database
1. Select "📚 Use Existing Database"
2. Choose from available knowledge bases
3. Start asking questions in the chat interface

### Creating New Database
1. Select "🆕 Create New Database" 
2. Enter a topic (e.g., "Python programming tutorials")
3. Wait for video discovery and processing
4. Chat with your new knowledge base

### Example Questions
- "What is MCP and how does it work?"
- "How do I create an MCP server?"
- "Can you show me a practical example?"
- "What are common MCP development challenges?"

## 🎯 Agent Engineering Bootcamp Requirements

This project fulfills the Week 2 homework requirements:

✅ **Two Distinct Tools**: YouTube Crawler + RAG Assistant  
✅ **Tool Integration**: Seamless workflow from content discovery to Q&A  
✅ **Practical Application**: Real-world YouTube content analysis  
✅ **User Interface**: Interactive Streamlit web application  
✅ **Documentation**: Comprehensive README and code comments  

## 🔄 Development Process

The project was built systematically:

1. **Reference Architecture Analysis** - Studied existing RAG implementation
2. **Tool 1 Development** - Built YouTube content crawler
3. **Tool 2 Development** - Implemented RAG knowledge assistant  
4. **Integration** - Combined tools into unified application
5. **Testing & Refinement** - Iterative improvement and debugging
6. **Documentation** - Created comprehensive project documentation

## 🚧 Known Issues

- Streamlit duplicate selectbox error on some runs (intermittent)
- LangChain deprecation warning for `get_relevant_documents` method
- Video count discrepancy (configured for 5, sometimes returns 6)

## 🔮 Future Enhancements

- Multi-language transcript support
- Video summarization capabilities
- Batch processing for large channels
- Export functionality for Q&A sessions
- Integration with additional video platforms

## 📝 License

This project is created for educational purposes as part of the Agent Engineering Bootcamp.

---

**Created by**: Danny  
**Course**: Agent Engineering Bootcamp Week 2  
**Date**: December 2024  
**Instructor Requirements**: Two-tool agent implementation
