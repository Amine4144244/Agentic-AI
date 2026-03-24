from config.groq_config import get_groq_response, MODELS


class ReActAgent:
    def __init__(self):
        self.name = "ReAct Agent"

    def process_query(self,query):
        messages = [
            {"role": "system", "content": """You are a ReAct agent that reasons step-by-step.
            Always respond in this format:
            Thought: <your reasoning>
            Action: <tool to use>
            Observation: <answer>"""},
            {"role": "user", "content": query}
        ]

        response = get_groq_response(messages, model=MODELS["reasoning"])
        return response