# 🤖 Agentic AI Tutorial - Powered by Groq API

A comprehensive demonstration of modern AI agent architectures, powered by **Groq LPU™ technology** for ultra-fast inference. This project showcases four core agentic patterns: **ReAct**, **RAG**, **Tool Use**, and **Workflow Orchestration**.

## 🚀 Overview

This tutorial-style application provides a hands-on experience with different types of AI agents. Whether you're interested in how agents reason (ReAct), how they use external data (RAG), how they interact with tools, or how they work together (Workflows), this project covers it all.

### Key Features
- **Ultra-fast Inference**: Leverages Groq's LPU™ technology for near-instant responses.
- **Multi-Agent Architecture**: Separate specialized agents for different task types.
- **Modern UI**: A sleek, responsive Streamlit dashboard.
- **Production-Ready Patterns**: Clean implementation of common agentic workflows.

---

## 🧠 Meet the Agents

### 1. ReAct Agent (Reasoning + Acting)
The ReAct agent combines reasoning and acting in a continuous loop. It thinks about the problem, decides on an action, observes the result, and iterates until it finds the final answer.
- **Best for**: Complex logic, multi-step reasoning, and math.

### 2. RAG Agent (Retrieval Augmented Generation)
This agent connects the LLM to your own data. It uses **ChromaDB** as a vector store and **Sentence Transformers** for local embeddings.
- **Capabilities**: Upload PDF/TXT/MD files, index them into a vector database, and query them with context-aware generation.

### 3. Tool Use Agent
An agent capable of "using" external tools to fetch real-time data or perform specific actions.
- **Available Tools**:
    - `get_stock_price`: Fetches real-time stock data using `yfinance`.
    - `calculate`: Evaluates mathematical expressions.

### 4. Workflow Orchestration Agent
The "Manager" agent. For complex tasks, it creates a step-by-step plan and orchestrates other agents/processes to complete the work.
- **Logic**: Planning -> Execution -> Synthesis.

---

## 🛠️ Tech Stack

- **Large Language Model**: [Groq API](https://groq.com/) (Llama 3.3, Mixtral)
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/)
- **Embeddings**: [HuggingFace Sentence Transformers](https://huggingface.co/sentence-transformers)
- **Data Tools**: YFinance, Plotly, Pandas

---

## 🏃‍♂️ Getting Started

### Prerequisites
- Python 3.9+
- A [Groq API Key](https://console.groq.com/)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Amine4144244/Agentic-AI.git
   cd Agentic-AI
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv agents-env
   source agents-env/bin/activate  # On Windows: agents-env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

### Running the App
Start the Streamlit dashboard:
```bash
streamlit run run.py
```

---

## 📂 Project Structure
```text
├── app/
│   └── agents/          # Agent implementations (ReAct, RAG, etc.)
├── config/
│   └── groq_config.py   # Groq API and Model configuration
├── run.py               # Main Streamlit application
├── .env                 # Environment variables (ignored by git)
├── .gitignore           # Git ignore rules
└── requirements.txt     # Python dependencies
```

## 📝 License
This project is for educational purposes. Feel free to use and adapt the patterns for your own applications!

---
*Built with ❤️ for the Agentic AI community.*
