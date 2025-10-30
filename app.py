# app.py
import streamlit as st
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
import chromadb

# --- Page Configuration ---
st.set_page_config(page_title="AI Property Assistant", page_icon="🤖", layout="wide")
st.title("🤖 AI Property Assistant")

# --- System Prompt for Conversational AI ---
# This prompt guides the LLM to be proactive and conversational,
# fulfilling your requirement for a more interactive bot.
SYSTEM_PROMPT = """
You are an expert real estate assistant named 'PropBot'.
Your primary goal is to help users find the perfect property.
You have access to a database of property listings.

**Your role is to be:**
1.  **Proactive & Conversational:** Don't just wait for filters. Ask clarifying questions to understand the user's needs, budget, and preferences (e.g., "What's your ideal commute?", "Are you looking for a quiet area or something near nightlife?").
2.  **Helpful & Suggestive:** Based on the conversation, retrieve relevant properties from your database and present them in a friendly, summarized way.
3.  **Data-Grounded:** ALL property suggestions MUST come from the retrieved context. Do not make up properties or details.
4.  **Natural:** Talk like a human assistant, not a database.

Start the conversation by introducing yourself and asking an open-ended question.
"""

@st.cache_resource
def load_chat_engine():
    """Loads the RAG chat engine from the persisted vector store."""
    
    # 1. Initialize ChromaDB
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("property_index")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    # 2. Load the Embedding Model
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    # 3. Load the index from the vector store
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model,
    )
    
    # 4. Initialize the Local LLM (Llama 3 via Ollama)
    llm = Ollama(model="llama3", request_timeout=120.0)
    
    # 5. Create the Chat Engine
    # We use a memory buffer to remember the conversation history
    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)
    
    chat_engine = ContextChatEngine.from_defaults(
        retriever=index.as_retriever(similarity_top_k=5), # Retrieve top 5 matching properties
        llm=llm,
        memory=memory,
        system_prompt=SYSTEM_PROMPT,
    )
    return chat_engine

# --- Main App Logic ---
try:
    chat_engine = load_chat_engine()
except Exception as e:
    st.error(f"Failed to load AI model or database. Please ensure 'Ollama' is running and you have run 'setup_vector_store.py'.\n\nError: {e}")
    st.stop()


# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm PropBot, your AI real estate assistant. What kind of property are you looking for today?"}]

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Accept user input
if prompt := st.chat_input("Ask me about properties..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # This is where the RAG engine is called
            response = chat_engine.chat(prompt)
            
            response_text = str(response)
            st.markdown(response_text)
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response_text})