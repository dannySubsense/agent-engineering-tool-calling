# YOUTUBE CHANNEL AGENT - MVP WITH ADVANCED CHAT
# Simple workflow: Topic → Top 5 Videos → Vector DB → Advanced Q&A Chat

import streamlit as st
import yaml
import os
import pandas as pd
from pathlib import Path

# YouTube API imports
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Advanced RAG imports
try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# PAGE CONFIG
st.set_page_config(
    page_title="YouTube Agent MVP", 
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 YouTube Channel Agent - MVP")
st.markdown("**Simple Workflow**: Topic → Top 5 Videos → Knowledge Base → Advanced Chat")

# LOAD CREDENTIALS
@st.cache_data
def load_credentials():
    try:
        with open('credentials.yml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        st.error(f"❌ Error loading credentials: {e}")
        st.stop()

credentials = load_credentials()
os.environ["OPENAI_API_KEY"] = credentials['openai']

# YOUTUBE CRAWLER CLASS
class YouTubeCrawler:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    def search_videos(self, query, max_results=5):
        """Search YouTube for top videos by topic"""
        try:
            # First, search for videos
            search_request = self.youtube.search().list(
                part='snippet',
                q=query,
                type='video',
                maxResults=max_results,
                order='relevance',
                videoDuration='medium'  # Filter out very short/long videos
            )
            search_response = search_request.execute()
            
            # Get video IDs for detailed info
            video_ids = [item['id']['videoId'] for item in search_response['items']]
            
            # Get detailed video information including duration
            details_request = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=','.join(video_ids)
            )
            details_response = details_request.execute()
            
            videos = []
            for item in details_response['items']:
                # Parse duration from ISO 8601 format (PT4M13S -> 4:13)
                duration_iso = item['contentDetails']['duration']
                duration_readable = self._parse_duration(duration_iso)
                
                video_data = {
                    'video_id': item['id'],
                    'title': item['snippet']['title'],
                    'channel': item['snippet']['channelTitle'],
                    'description': item['snippet']['description'][:200] + "...",
                    'published_at': item['snippet']['publishedAt'],
                    'duration': duration_readable,
                    'duration_iso': duration_iso,
                    'view_count': int(item['statistics'].get('viewCount', 0)),
                    'like_count': int(item['statistics'].get('likeCount', 0)),
                    'thumbnail_url': item['snippet']['thumbnails']['medium']['url'],
                    'url': f"https://youtube.com/watch?v={item['id']}"
                }
                videos.append(video_data)
            
            return videos
        except Exception as e:
            st.error(f"YouTube API Error: {e}")
            return []
    
    def _parse_duration(self, duration_iso):
        """Convert ISO 8601 duration to readable format (PT4M13S -> 4:13)"""
        import re
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_iso)
        if not match:
            return "Unknown"
        
        hours, minutes, seconds = match.groups()
        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0
        seconds = int(seconds) if seconds else 0
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    def get_transcript(self, video_id):
        """Get transcript for a video"""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([entry['text'] for entry in transcript_list])
            return transcript_text
        except Exception as e:
            return f"Transcript not available: {str(e)}"
    
    def process_videos(self, videos):
        """Process videos and extract transcripts"""
        processed_data = []
        
        st.subheader("📝 Processing Videos...")
        progress_bar = st.progress(0)
        
        for i, video in enumerate(videos):
            with st.expander(f"Processing: {video['title'][:60]}..."):
                st.write(f"**Channel:** {video['channel']}")
                st.write(f"**Duration:** {video['duration']}")
                st.write(f"**Views:** {video['view_count']:,}")
                st.write(f"**URL:** {video['url']}")
                
                # Get transcript
                transcript = self.get_transcript(video['video_id'])
                
                if "Transcript not available" in transcript:
                    st.warning("⚠️ No transcript available")
                else:
                    st.success("✅ Transcript extracted")
                    st.write(f"**Preview:** {transcript[:200]}...")
                
                processed_data.append({
                    'video_id': video['video_id'],
                    'title': video['title'],
                    'channel': video['channel'],
                    'description': video['description'],
                    'published_at': video['published_at'],
                    'duration': video['duration'],
                    'duration_iso': video['duration_iso'],
                    'view_count': video['view_count'],
                    'like_count': video['like_count'],
                    'thumbnail_url': video['thumbnail_url'],
                    'transcript': transcript,
                    'url': video['url']
                })
            
            progress_bar.progress((i + 1) / len(videos))
        
        return processed_data

# RAG SYSTEM CLASS
class AdvancedRAG:
    def __init__(self):
        self.embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    def load_existing_database(self, topic):
        """Load existing vector database if it exists"""
        db_path = f"data/mvp_{topic.replace(' ', '_')}_db"
        if os.path.exists(db_path):
            try:
                vectorstore = Chroma(
                    persist_directory=db_path,
                    embedding_function=self.embedding_function
                )
                return vectorstore, db_path
            except Exception as e:
                st.warning(f"Could not load existing database: {e}")
                return None, None
        return None, None
    
    def create_knowledge_base(self, processed_data, topic):
        """Create vector database from video transcripts"""
        documents = []
        metadatas = []
        
        for item in processed_data:
            if "Transcript not available" not in item['transcript']:
                # Chunk the transcript
                transcript = item['transcript']
                chunk_size = 1000
                
                for i in range(0, len(transcript), chunk_size):
                    chunk = transcript[i:i + chunk_size]
                    documents.append(chunk)
                    metadatas.append({
                        'title': item['title'],
                        'channel': item['channel'],
                        'video_id': item['video_id'],
                        'url': item['url'],
                        'duration': item.get('duration', 'Unknown'),
                        'view_count': item.get('view_count', 0),
                        'like_count': item.get('like_count', 0),
                        'published_at': item.get('published_at', ''),
                        'topic': topic
                    })
        
        if not documents:
            st.error("❌ No valid transcripts found to create knowledge base")
            return None
        
        # Create vector store
        db_path = f"data/mvp_{topic.replace(' ', '_')}_db"
        vectorstore = Chroma.from_texts(
            texts=documents,
            metadatas=metadatas,
            embedding=self.embedding_function,
            persist_directory=db_path
        )
        
        st.success(f"✅ Knowledge base created with {len(documents)} text chunks")
        return vectorstore, db_path
    
    def create_advanced_rag_chain(self, vectorstore, topic):
        """Create history-aware RAG chain with memory integration"""
        try:
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            
            # STAGE 1: History-aware question contextualization
            contextualize_q_system_prompt = f"""Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is.

Focus on {topic} concepts and YouTube video content."""
            
            contextualize_q_prompt = ChatPromptTemplate.from_messages([
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])
            
            # Create history-aware retriever
            history_aware_retriever = create_history_aware_retriever(
                self.llm, retriever, contextualize_q_prompt
            )
            
            # STAGE 2: Answer generation with context and history
            qa_system_prompt = f"""You are an expert YouTube Channel Agent with access to a curated database of {topic} videos.

You have access to full video transcripts and complete metadata for each source. The context includes both the video content and all available metadata about each video source.

When answering questions, you can reference any information available in the context, including video content, metadata, and source details. Use this information to provide comprehensive, accurate responses.

ALWAYS draw from the video content and source metadata in your responses. Use all available information from the context to give specific, detailed answers.

Context from videos:
{{context}}"""
            
            qa_prompt = ChatPromptTemplate.from_messages([
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ])
            
            # Create question-answer chain
            question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
            
            # Combine into full RAG chain
            rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
            
            return rag_chain
            
        except Exception as e:
            st.error(f"❌ Error creating advanced RAG chain: {e}")
            return None

# MAIN APPLICATION
def main():
    # DATABASE SELECTION OR CREATION
    st.header("🔍 Select Database or Create New")
    
    # Check for existing databases
    rag = AdvancedRAG()
    available_databases = ["VIBE CODING MCP DEVELOPMENT TUTORIAL"]  # Could be expanded to scan for all databases
    
    # Database selection options
    database_option = st.radio(
        "Choose your option:",
        ["📚 Use Existing Database", "🆕 Create New Database"],
        horizontal=True,
        help="Select an existing database or create a new one with different content"
    )
    
    if database_option == "📚 Use Existing Database":
        # Dropdown for existing databases
        selected_db = st.selectbox(
            "Select database:",
            available_databases,
            help="Choose from available knowledge bases",
            key="database_selector"
        )
        topic = selected_db
        if 'creating_new' in st.session_state:
            del st.session_state.creating_new
            
    else:  # Create New Database
        st.session_state.creating_new = True
        
        # Inline topic input with immediate action
        with st.container():
            topic = st.text_input(
                "Enter topic for new database:", 
                value="",
                placeholder="e.g., Python programming tutorials, React development, Machine Learning basics, etc.",
                help="⚠️ Enter a NEW topic. This will create a completely new knowledge base with different YouTube videos",
                key="new_topic_input"
            )
            
            # Validation and immediate action in the same section
            if not topic.strip():
                st.info("👆 Enter a topic above to enable knowledge base creation")
            elif topic.strip() in available_databases:
                st.error(f"⚠️ Database '{topic.strip()}' already exists! Please enter a different topic.")
                topic = ""  # Clear the topic to prevent proceeding
            else:
                # Valid topic - show create button immediately
                if st.button(f"🚀 Create Knowledge Base: '{topic}'", type="primary", key="create_new_db_button"):
                    st.session_state.proceed_with_creation = True
                    st.session_state.creation_topic = topic
    
    if not topic:
        return
    
    # Load the database for the selected/entered topic
    if not hasattr(rag, 'load_existing_database'):  # rag was already created above
        rag = AdvancedRAG()
    current_db, current_db_path = rag.load_existing_database(topic)
    
    if current_db:
        st.session_state.vectorstore = current_db
        st.session_state.topic = topic
        
        # Show content summary
        with st.expander("📚 Content Summary - See what's in your knowledge base"):
            # Add cache clearing button for debugging
            if st.button("🔄 Refresh Data", help="Clear cache and reload database info", key="refresh_data"):
                st.cache_data.clear()
                st.rerun()
                
            try:
                # Get ALL documents directly from the collection - no similarity search needed
                collection = current_db._collection
                all_results = collection.get(include=['metadatas'])
                
                # Extract unique videos from metadata
                videos_info = {}
                for metadata in all_results['metadatas']:
                    title = metadata.get('title', 'Unknown')
                    channel = metadata.get('channel', 'Unknown')
                    url = metadata.get('url', '#')
                    duration = metadata.get('duration', 'Unknown')
                    view_count = metadata.get('view_count', 0)
                    
                    if title not in videos_info and title != 'Unknown':
                        videos_info[title] = {
                            'channel': channel,
                            'url': url,
                            'duration': duration,
                            'view_count': view_count
                        }
                
                st.markdown(f"**📹 Videos in Database:** {len(videos_info)}")
                st.markdown(f"**📄 Total Document Chunks:** {collection.count()}")
                
                # Debug info
                with st.expander("🔍 Debug Info"):
                    st.write(f"Collection ID: {collection.id}")
                    st.write(f"Total metadata entries: {len(all_results['metadatas'])}")
                    st.write("Sample titles found:")
                    for i, title in enumerate(sorted(videos_info.keys())):
                        st.write(f"{i+1}. {title}")
                
                # Overall summary and key insights
                st.markdown("### 📋 Knowledge Base Summary:")
                st.markdown(f"""
                **Your knowledge base contains comprehensive MCP (Model Context Protocol) development tutorials** covering everything from basic concepts to advanced implementation techniques. The content spans **{len(videos_info)} tutorial videos from Vibe Coding** that provide both theoretical understanding and practical hands-on experience.
                
                **🎯 Core Topics Covered:**
                • **MCP Protocol Fundamentals** - What MCP is, how it works, and why it's important for AI development
                • **Server Creation Workflows** - Multiple approaches from 5-prompt quick builds to detailed 10-minute tutorials  
                • **API Integration Techniques** - How to connect external APIs and data sources to your MCP server
                • **Beginner-Friendly Guidance** - Complete starter tutorials for developers new to MCP
                • **Development Philosophy** - Understanding the "vibe coding" approach and mindset for rapid prototyping
                
                **💡 Key Learning Outcomes:**
                After exploring this knowledge base, you'll understand how to build MCP servers from scratch, integrate external APIs, follow best practices for rapid development, and avoid common pitfalls. The tutorials emphasize practical implementation over theory, making complex concepts accessible to beginners while providing valuable insights for experienced developers.
                """)
                
                st.markdown("### 📺 Videos Available:")
                for i, (title, info) in enumerate(videos_info.items(), 1):
                    view_count_formatted = f"{info['view_count']:,}" if info['view_count'] > 0 else "N/A"
                    st.markdown(f"""
                    **{i}. {title}**  
                    👤 *{info['channel']}* | ⏱️ {info['duration']} | 👁️ {view_count_formatted} views | [🔗 Watch Video]({info['url']})
                    """)
                    
            except Exception as e:
                st.warning(f"Could not load content summary: {e}")
                st.write(f"Debug info: {str(e)}")
                # Show more debug details
                st.write("Database object:", type(current_db))
                if hasattr(current_db, '_collection'):
                    st.write("Collection object:", type(current_db._collection))
                else:
                    st.write("No _collection attribute found")
        
        st.info("💡 **Ready to use!** Jump to the chat below, or create a new knowledge base.")
    
    # SEARCH & PROCESS (show when creating new database)
    elif hasattr(st.session_state, 'creating_new') and st.session_state.creating_new:
        st.header("🚀 Search & Build Knowledge Base")
        st.info(f"Creating new knowledge base for: **{topic}**")
        # The creation button is already handled in Step 1
    
    # Process the creation if user clicked any create button
    if hasattr(st.session_state, 'proceed_with_creation') and st.session_state.proceed_with_creation:
        del st.session_state.proceed_with_creation  # Clear the flag
        creation_topic = st.session_state.get('creation_topic', topic)
        if 'creation_topic' in st.session_state:
            del st.session_state.creation_topic
        crawler = YouTubeCrawler(credentials['youtube'])
        
        # Search videos
        with st.spinner(f"🔍 Searching YouTube for: '{creation_topic}'"):
            videos = crawler.search_videos(creation_topic, max_results=5)
        
        if not videos:
            st.error("No videos found for this topic. Try a different search term.")
            return
        
        st.success(f"✅ Found {len(videos)} videos!")
        
        # Process videos
        processed_data = crawler.process_videos(videos)
        
        # Create knowledge base
        st.header("🧠 Building Knowledge Base")
        with st.spinner("Creating vector database..."):
            result = rag.create_knowledge_base(processed_data, creation_topic)
            
            if result:
                vectorstore, db_path = result
                st.session_state.vectorstore = vectorstore
                st.session_state.topic = creation_topic
                st.success("🎉 Knowledge base ready! You can now chat below.")
    
    # CHAT WITH YOUR AGENT
    if hasattr(st.session_state, 'vectorstore'):
        st.header("💬 Chat with Your Agent")
        
        # Show topic info
        st.info(f"📚 Knowledge Base: **{st.session_state.topic}** | Ready for questions!")
        
        # Initialize chat memory
        msgs = StreamlitChatMessageHistory(key="chat_messages")
        if len(msgs.messages) == 0:
            msgs.add_ai_message(f"""👋 Hi! I'm your YouTube Channel Agent with access to **5 MCP development tutorial videos** from Vibe Coding!

I have detailed knowledge from these videos:
🎥 "Build An MCP Server In 5 Prompts" 
🎥 "Let's Vibe Code an MCP Server in 10 Minutes"
🎥 "Let's Vibe Code any API into our MCP server"
🎥 "The 'vibe coding' mind virus explained"
🎥 "Vibe Coding an MCP Server (As a Complete Beginner)"

I can help you with:
✅ Step-by-step MCP server creation
✅ Code examples and implementation details  
✅ API integration techniques
✅ Best practices from the tutorials

What would you like to learn about MCP development?""")
        
        # Create RAG chain (fix the error)
        if 'rag_chain' not in st.session_state:
            with st.spinner("🧠 Initializing chat system..."):
                try:
                    st.session_state.rag_chain = rag.create_advanced_rag_chain(st.session_state.vectorstore, st.session_state.topic)
                    if st.session_state.rag_chain is None:
                        st.error("❌ Failed to initialize chat system")
                        return
                except Exception as e:
                    st.error(f"❌ Error initializing chat: {e}")
                    return
        
        # Quick Questions (better positioned)
        with st.expander("💡 Quick Questions - Click to Ask"):
            # Generate contextual quick questions based on topic
            if "MCP" in st.session_state.topic.upper():
                quick_questions = [
                    "What is MCP and how does it work?",
                    "How do I create an MCP server?",
                    "What are the key components of MCP?",
                    "Can you show me a practical example?",
                    "What are common MCP development challenges?"
                ]
            else:
                quick_questions = [
                    f"What are the key concepts in {st.session_state.topic}?",
                    "Can you summarize the main points?",
                    "What are the best practices mentioned?",
                    "How do I get started with this topic?",
                    "What are common challenges discussed?"
                ]
            
            # Display questions in columns for better layout
            cols = st.columns(2)
            for i, q in enumerate(quick_questions):
                with cols[i % 2]:
                    if st.button(q, key=f"quick_{hash(q)}", use_container_width=True):
                        # Process the question immediately
                        st.session_state.quick_question = q
                        st.rerun()
        
        # Chat management
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**💬 Chat Messages:** {len(msgs.messages)}")
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                msgs.clear()
                msgs.add_ai_message(f"👋 Chat cleared! I'm ready for a fresh conversation about {st.session_state.topic}.")
                st.rerun()
        
        # Handle quick question if one was clicked
        if hasattr(st.session_state, 'quick_question'):
            question = st.session_state.quick_question
            delattr(st.session_state, 'quick_question')
            
            # Add to history first
            msgs.add_user_message(question)
            
            # Generate response with history awareness
            try:
                # Wrap RAG chain with message history
                rag_with_history = RunnableWithMessageHistory(
                    st.session_state.rag_chain,
                    lambda session_id: msgs,
                    input_messages_key="input",
                    history_messages_key="chat_history",
                    output_messages_key="answer",
                )
                
                # Invoke the advanced RAG chain
                response = rag_with_history.invoke(
                    {"input": question},
                    config={"configurable": {"session_id": "youtube_agent"}}
                )
                
                # Add response to history
                msgs.add_ai_message(response['answer'])
                
                # Store sources for display
                if 'context' in response and response['context']:
                    sources_seen = set()
                    sources_text = "**📚 Sources Used:**\n"
                    for doc in response['context']:
                        title = doc.metadata.get('title', 'Unknown')
                        channel = doc.metadata.get('channel', 'Unknown')
                        url = doc.metadata.get('url', '#')
                        
                        source_key = f"{title}|{channel}"
                        if source_key not in sources_seen:
                            sources_text += f"- **{title}** by {channel} - [🔗 Watch]({url})\n"
                            sources_seen.add(source_key)
                    
                    # Add sources as a separate message
                    msgs.add_ai_message(sources_text)
                
                # Trigger rerun to show the new messages
                st.rerun()
                
            except Exception as e:
                error_msg = f"❌ Error processing question: {e}"
                msgs.add_ai_message(error_msg)
                st.rerun()
        
        # Display chat history
        for msg in msgs.messages:
            with st.chat_message(msg.type):
                st.markdown(msg.content)

        # PROMINENT CHAT INPUT
        st.markdown("### 💬 Ask Your Question:")
        if question := st.chat_input(f"Type your question about {st.session_state.topic} here... (I remember our conversation!)"):
            # Add to history first
            msgs.add_user_message(question)
            
            # Generate response with history awareness
            try:
                # Wrap RAG chain with message history
                rag_with_history = RunnableWithMessageHistory(
                    st.session_state.rag_chain,
                    lambda session_id: msgs,
                    input_messages_key="input",
                    history_messages_key="chat_history",
                    output_messages_key="answer",
                )
                
                # Invoke the advanced RAG chain
                response = rag_with_history.invoke(
                    {"input": question},
                    config={"configurable": {"session_id": "youtube_agent"}}
                )
                
                # Add response to history
                msgs.add_ai_message(response['answer'])
                
                # Store sources for display
                if 'context' in response and response['context']:
                    sources_seen = set()
                    sources_text = "**📚 Sources Used:**\n"
                    for doc in response['context']:
                        title = doc.metadata.get('title', 'Unknown')
                        channel = doc.metadata.get('channel', 'Unknown')
                        url = doc.metadata.get('url', '#')
                        
                        source_key = f"{title}|{channel}"
                        if source_key not in sources_seen:
                            sources_text += f"- **{title}** by {channel} - [🔗 Watch]({url})\n"
                            sources_seen.add(source_key)
                    
                    # Add sources as a separate message
                    msgs.add_ai_message(sources_text)
                
                # Trigger rerun to show the new messages
                st.rerun()
                
            except Exception as e:
                error_msg = f"❌ Error processing question: {e}"
                msgs.add_ai_message(error_msg)
                st.rerun()
    
    # FOOTER
    st.markdown("---")
    st.markdown("**YouTube Channel Agent MVP** | Agent Engineering Bootcamp Week 2")

if __name__ == "__main__":
    main() 