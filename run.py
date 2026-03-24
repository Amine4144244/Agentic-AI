#!/usr/bin/env python3
"""
Agentic AI Tutorial - Powered by Groq API
A comprehensive demonstration of ReAct, RAG, Tool Use, and Workflow Orchestration
"""

import streamlit as st
import os
import sys
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our agent modules
from config.groq_config import get_groq_response, MODELS, test_groq_connection
from app.agents.react_agent import ReActAgent
from app.agents.rag_agent import RAGAgent
from app.agents.tool_agent import ToolAgent
from app.agents.workflow_agent import WorkflowAgent

# Page configuration
st.set_page_config(
    page_title="Agentic AI Tutorial - Groq Edition",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'react_agent' not in st.session_state:
        st.session_state.react_agent = ReActAgent()
    if 'rag_agent' not in st.session_state:
        st.session_state.rag_agent = RAGAgent()
    if 'tool_agent' not in st.session_state:
        st.session_state.tool_agent = ToolAgent()
    if 'workflow_agent' not in st.session_state:
        st.session_state.workflow_agent = WorkflowAgent()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'api_connected' not in st.session_state:
        st.session_state.api_connected = test_groq_connection()

# Sidebar with configuration
def render_sidebar():
    """Render the sidebar with configuration and metrics"""
    with st.sidebar:
        st.image("https://groq.com/wp-content/uploads/2024/03/Groq-Logo.svg", use_container_width=True)
        st.markdown("---")
        
        # API Status
        st.subheader("🔌 API Status")
        if st.session_state.api_connected:
            st.success("✅ Groq API Connected")
            st.info(f"Model: {MODELS['reasoning']}")
        else:
            st.error("❌ Groq API Not Connected")
            st.warning("Please check your API key in .env file")
        
        st.markdown("---")
        
        # Model Selection
        st.subheader("🎛️ Model Configuration")
        selected_model = st.selectbox(
            "Select Model",
            options=list(MODELS.keys()),
            format_func=lambda x: f"{x.title()}: {MODELS[x]}"
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.05,
            help="Higher = more creative, Lower = more focused"
        )
        
        max_tokens = st.slider(
            "Max Tokens",
            min_value=100,
            max_value=4096,
            value=1024,
            step=100
        )
        
        st.markdown("---")
        
        # Usage Statistics
        st.subheader("📊 Session Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Queries", len(st.session_state.chat_history))
        with col2:
            st.metric("Agents", "4 Active")
        
        st.markdown("---")
        
        # Clear History Button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown("---")
        st.caption("Powered by Groq LPU™ Technology")
        st.caption(f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ReAct Agent Tab
def render_react_tab():
    """Render the ReAct agent interface"""
    st.header("🧠 ReAct Agent (Reasoning + Acting)")
    st.markdown("""
    The ReAct agent combines reasoning and acting in a loop. It:
    1. **Thought**: Analyzes the problem
    2. **Action**: Decides what tool/action to use
    3. **Observation**: Observes the result
    4. **Final Answer**: Provides the solution
    """)
    
    # Input area
    query = st.text_area(
        "Ask a complex reasoning question:",
        placeholder="Example: What's 15% of 320 plus the square root of 144?",
        height=100
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        submit = st.button("🧠 Run ReAct", type="primary")
    
    if submit and query:
        with st.spinner("🤔 Agent is reasoning..."):
            try:
                # Get ReAct response
                response = st.session_state.react_agent.process_query(query)
                
                # Display results
                st.markdown("### 💡 Agent Response")
                st.markdown(response)
                
                # Add to history
                st.session_state.chat_history.append({
                    "agent": "ReAct",
                    "query": query,
                    "response": response,
                    "timestamp": datetime.now()
                })
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display example queries
    with st.expander("📝 Example Queries"):
        st.markdown("""
        - "What's the square root of 144 multiplied by 10?"
        - "If I invest $1000 with 5% annual interest, what's the value after 3 years?"
        - "Calculate the compound interest on $5000 at 8% for 2 years"
        """)

# RAG Agent Tab
def render_rag_tab():
    """Render the RAG agent interface"""
    st.header("📚 RAG Agent (Retrieval Augmented Generation)")
    st.markdown("""
    The RAG agent combines document retrieval with generation:
    1. **Index Documents**: Load documents into vector database
    2. **Retrieve**: Find relevant information
    3. **Generate**: Answer based on retrieved context
    """)
    
    # Document upload section
    with st.expander("📄 Upload Documents", expanded=False):
        uploaded_files = st.file_uploader(
            "Upload documents for RAG",
            type=['txt', 'pdf', 'md'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            if st.button("📚 Index Documents"):
                with st.spinner("Indexing documents..."):
                    for file in uploaded_files:
                        content = file.read().decode()
                        st.session_state.rag_agent.add_document(content, file.name)
                    st.success(f"Indexed {len(uploaded_files)} documents!")
    
    # Query section
    query = st.text_area(
        "Ask a question about your documents:",
        placeholder="Example: What are the key findings?",
        height=100
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        submit = st.button("🔍 Query RAG", type="primary")
    
    if submit and query:
        with st.spinner("Searching documents and generating response..."):
            try:
                # Get RAG response
                response, sources = st.session_state.rag_agent.query(query)
                
                # Display results
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("### 💡 Answer")
                    st.markdown(response)
                
                with col2:
                    st.markdown("### 📑 Sources")
                    for i, source in enumerate(sources[:3], 1):
                        st.info(f"Source {i}: {source}")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Tool Agent Tab
def render_tools_tab():
    """Render the tool use agent interface"""
    st.header("🛠️ Tool Use Agent")
    st.markdown("""
    The agent can use various tools to accomplish tasks:
    - **Stock Price**: Get real-time stock data
    - **Calculator**: Perform calculations
    - **Web Search**: Search the internet
    - **Weather**: Get weather information
    """)
    
    # Available tools display
    st.subheader("🔧 Available Tools")
    tools = st.session_state.tool_agent.list_tools()
    
    cols = st.columns(4)
    for idx, (tool_name, tool_desc) in enumerate(tools.items()):
        with cols[idx % 4]:
            st.info(f"**{tool_name}**\n{tool_desc}")
    
    st.markdown("---")
    
    # Query input
    query = st.text_area(
        "Ask the agent to use a tool:",
        placeholder="Example: Get me Apple's stock price",
        height=100
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        submit = st.button("🔧 Execute", type="primary")
    
    if submit and query:
        with st.spinner("Using tools..."):
            try:
                # Process with tool agent
                result = st.session_state.tool_agent.process_query(query)
                
                st.markdown("### 🔧 Tool Execution Result")
                st.markdown(result)
                
                # Show tool usage metrics
                if hasattr(st.session_state.tool_agent, 'last_tool_used'):
                    st.info(f"Used tool: {st.session_state.tool_agent.last_tool_used}")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Workflow Agent Tab
def render_workflow_tab():
    """Render the workflow orchestration interface"""
    st.header("⚙️ Workflow Orchestration Agent")
    st.markdown("""
    The workflow agent orchestrates multiple agents to complete complex tasks:
    1. **Planning**: Creates a step-by-step plan
    2. **Execution**: Uses appropriate agents/tools
    3. **Synthesis**: Combines results into coherent output
    """)
    
    # Complex task input
    task = st.text_area(
        "Enter a complex task:",
        placeholder="Example: Analyze Apple stock and provide investment recommendation",
        height=100
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        submit = st.button("⚙️ Run Workflow", type="primary")
    
    if submit and task:
        with st.spinner("Orchestrating multi-agent workflow..."):
            try:
                # Execute workflow
                result = st.session_state.workflow_agent.execute_workflow(task)
                
                # Display results in tabs
                tabs = st.tabs(["Final Output", "Execution Steps", "Agent Contributions"])
                
                with tabs[0]:
                    st.markdown(result.get('final_output', 'No output generated'))
                
                with tabs[1]:
                    steps = result.get('steps', [])
                    for i, step in enumerate(steps, 1):
                        with st.expander(f"Step {i}: {step.get('agent', 'Unknown')}"):
                            st.markdown(f"**Task:** {step.get('task', 'N/A')}")
                            st.markdown(f"**Result:** {step.get('result', 'N/A')}")
                
                with tabs[2]:
                    contributions = result.get('contributions', {})
                    for agent, contribution in contributions.items():
                        st.metric(agent, contribution)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Chat Tab
def render_chat_tab():
    """Render the chat interface"""
    st.header("💬 Agent Chat")
    st.markdown("Chat with all agents working together!")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message("assistant"):
            st.markdown(f"**{message['agent']} Agent**")
            st.markdown(message['response'])
            st.caption(message['timestamp'].strftime("%H:%M:%S"))
    
    # Chat input
    if prompt := st.chat_input("Ask anything..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                # Determine which agent to use based on query
                query_lower = prompt.lower()
                
                if any(word in query_lower for word in ['calculate', 'math', 'solve']):
                    response = st.session_state.react_agent.process_query(prompt)
                    agent = "ReAct"
                elif any(word in query_lower for word in ['document', 'file', 'rag']):
                    response, _ = st.session_state.rag_agent.query(prompt)
                    agent = "RAG"
                elif any(word in query_lower for word in ['stock', 'price', 'weather', 'search']):
                    response = st.session_state.tool_agent.process_query(prompt)
                    agent = "Tool"
                else:
                    # Use workflow for complex tasks
                    result = st.session_state.workflow_agent.execute_workflow(prompt)
                    response = result.get('final_output', prompt)
                    agent = "Workflow"
                
                st.markdown(f"**{agent} Agent**")
                st.markdown(response)
                
                # Save to history
                st.session_state.chat_history.append({
                    "agent": agent,
                    "query": prompt,
                    "response": response,
                    "timestamp": datetime.now()
                })

# Main App
def main():
    """Main application entry point"""
    
    # Initialize session
    init_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    st.markdown('<div class="main-header">Agentic AI Tutorial</div>', unsafe_allow_html=True)
    st.markdown("*Powered by Groq LPU™ - Ultra-fast inference*")
    
    # Create tabs
    tabs = st.tabs([
        "🧠 ReAct",
        "📚 RAG",
        "🛠️ Tools",
        "⚙️ Workflow",
        "💬 Chat"
    ])
    
    with tabs[0]:
        render_react_tab()
    
    with tabs[1]:
        render_rag_tab()
    
    with tabs[2]:
        render_tools_tab()
    
    with tabs[3]:
        render_workflow_tab()
    
    with tabs[4]:
        render_chat_tab()
    
    # Footer
    st.markdown("---")
    st.caption("Built with Streamlit + Groq API | Learn agentic AI patterns: ReAct, RAG, Tools, Workflows")

if __name__ == "__main__":
    main()