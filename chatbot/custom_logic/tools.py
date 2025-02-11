from langchain_core.tools import Tool
from custom_logic.utils import generate_tool_description 

def fibonacci(n):
    """Calculates the Fibonacci sequence for a given number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def run_fibonacci_tool(n):
    """Wrapper function for LangChain"""
    result = fibonacci(int(n))
    return f"Final Answer: {result}"

# ✅ Use the generic function to create the tool description
fibonacci_tool = Tool(
    name="Fibonacci Calculator",
    func=run_fibonacci_tool,
    description=generate_tool_description(
        name="Fibonacci Calculator",
        input_format="<number>",
        example_input="Calculate Fibonacci of 10",
        example_output="55"
    )
)
