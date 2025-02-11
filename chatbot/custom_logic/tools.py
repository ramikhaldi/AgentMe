from langchain.tools import Tool

def fibonacci(n):
    """Custom Fibonacci function."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def run_fibonacci_tool(n):
    """Wrapper function for LangChain"""
    return {"result": fibonacci(int(n))}

fibonacci_tool = Tool(
    name="Fibonacci Calculator",
    func=run_fibonacci_tool,
    description="Calculates the Fibonacci sequence for a given number."
)
