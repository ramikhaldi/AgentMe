from langchain_core.tools import Tool
from utils import generate_tool_description

def fibonacci(n):
    """Calculates the Fibonacci sequence for a given number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def run_fibonacci_tool(n):
    """Wrapper function for LangChain"""
    result = fibonacci(int(n))
    return f"Final Answer: {result}"

fibonacci_tool = Tool(
    name="Fibonacci Calculator",
    func=run_fibonacci_tool,
    description=f"Call this tool if a Fibonacci of number has to be computed. Use 'Action: Fibonacci Calculator' and pass the input as 'Action Input: <number>'.\n"
)
