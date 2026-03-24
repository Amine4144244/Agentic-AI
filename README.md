# Agentic AI with Groq

This is a project I put together to experiment with different AI agent patterns—specifically ReAct, RAG, and multi-agent workflows—using Groq's API for fast inference. 

The goal was to build a simple, interactive dashboard where you can see how these agents actually work under the hood.

## What's inside?

- **ReAct Agent**: A basic implementation of reasoning and acting. It thinks through a problem step-by-step before giving an answer.
- **RAG Agent**: Uses ChromaDB and Sentence Transformers to let you upload your own documents and ask questions about them.
- **Tools**: I've added a few basic tools like a calculator and a stock price fetcher (via yfinance) that the agents can use.
- **Workflows**: A manager-style agent that tries to plan out and execute more complex tasks.

## Getting it running

If you want to try it out yourself, here's the setup:

1. **Clone & Install**:
   ```bash
   git clone https://github.com/Amine4144244/Agentic-AI.git
   cd Agentic-AI
   pip install -r requirements.txt
   ```

2. **Environment**:
   You'll need a Groq API key. Create a `.env` file in the root and add it:
   ```text
   GROQ_API_KEY=your_key_here
   ```

3. **Launch**:
   Run the Streamlit app:
   ```bash
   streamlit run run.py
   ```

## A few notes

- The embeddings for the RAG agent are handled locally using `SentenceTransformer`, so you don't need a separate API for that.
- I've primarily used Llama 3 and Mixtral models for the different agents.
- The UI is built with Streamlit because it's the easiest way to get a dashboard up and running quickly.

Feel free to poke around the code in `app/agents/` to see how the logic is structured.
