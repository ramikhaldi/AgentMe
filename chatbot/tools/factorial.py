from langchain_core.tools import Tool
from utils import generate_tool_description

def factorial(n):
    """Calculates the factorial of a given number."""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def run_factorial_tool(n):
    """Wrapper function for LangChain"""
    result = factorial(int(n))
    return f"Final Answer: {result}"

factorial_tool = Tool(
    name="Factorial Calculator",
    func=run_factorial_tool,
    description=f"Call this tool if a factorial of number has to be computed. Use 'Action: Factorial Calculator' and pass the input as 'Action Input: <number>'.\n"
)
