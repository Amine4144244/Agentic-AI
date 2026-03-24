import json
import yfinance as yf
from config.groq_config import get_groq_response, MODELS

class ToolAgent:
    def __init__(self):
        self.name = "Tool Agent"
        self.tools = {
            "get_stock_price": lambda ticker: yf.Ticker(ticker).info.get('regularMarketPrice'),
            "calculate": lambda expr: eval(expr)
        }

    def list_tools(self):
        """List available tools and their descriptions"""
        return {
            "get_stock_price": "Get current stock price (args: ticker)",
            "calculate": "Evaluate math expression (args: expr)"
        }

    def process_query(self, query):
        """Process a query using available tools"""
        messages = [
            {"role": "system", "content": """You have access to tools:
            -get_stock_price(ticker): Get current stock price
            -calculate(expr): Evaluate math expression
            
            Respond in JSON format: {"tool": "tool_name", "args": {"arg1": "val1"}}"""},
            {"role": "user", "content": query}
        ]

        response = get_groq_response(messages, model=MODELS["tool"])

        try:
            tool_call = json.loads(response)
            tool_name = tool_call.get("tool")
            args = tool_call.get("args", {})
            
            if tool_name in self.tools:
                result = self.tools[tool_name](**args)
                self.last_tool_used = tool_name
                return f"Tool result: {result}"
            else:
                return f"Tool '{tool_name}' not found."
        except Exception as e:
            return f"Error executing tool: {str(e)}\nResponse was: {response}"