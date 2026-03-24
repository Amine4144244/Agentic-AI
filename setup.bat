@echo off
echo  Setting up Groq Agentic AI Project

echo  Creating virtual environment...
python -m venv groq-venv

echo  Activating virtual environment...
call groq-venv\Scripts\activate.bat

echo  Upgrading pip...
python -m pip install --upgrade pip

echo  Installing requirements...
pip install -r requirements.txt

echo  Creating .env file template...
if not exist .env (
    echo GROQ_API_KEY=your_api_key_here > .env
    echo Please edit .env and add your Groq API key
)

echo  Setup complete!
echo  To activate the environment: groq-venv\Scripts\activate
echo  To run the app: streamlit run run.py