from config.groq_config import get_groq_response, MODELS

class WorkflowAgent:
    def __init__(self):
        self.name = "Workflow Agent"

    def execute_workflow(self, task):
        """Orchestrate a multi-agent workflow for a complex task"""
        # 1. Planning
        plan_prompt = f"""Create a step-by-step plan to solve this task: {task}
        Respond with a numbered list of steps."""
        plan = get_groq_response([{"role": "user", "content": plan_prompt}], model=MODELS["reasoning"])
        
        # 2. Execution (Simulated for this demo)
        execution_prompt = f"Executing the following plan: {plan}\nTask: {task}"
        result = get_groq_response([{"role": "user", "content": execution_prompt}], model=MODELS["fast"])
        
        # 3. Final Output & Metrics
        return {
            "final_output": result,
            "steps": [
                {"agent": "Planner", "task": "Create plan", "result": plan},
                {"agent": "Executor", "task": "Execute plan", "result": result}
            ],
            "contributions": {
                "Planner": 1,
                "Executor": 1
            }
        }
