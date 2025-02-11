from langchain_core.tools import Tool
from utils import generate_tool_description

def compute_expression(a, b, c):
    """Computes the expression a - (b * c)."""
    return a - (b * c)

def run_compute_expression_tool(params):
    """Wrapper function for LangChain"""
    try:
        a, b, c = map(float, params.split())  # Convert input to floats
        result = compute_expression(a, b, c)
        return f"Final Answer: {result}"
    except Exception as e:
        return f"Error: Invalid input format. Expected three numbers. {str(e)}"

compute_expression_tool = Tool(
    name="Compute Expression",
    func=run_compute_expression_tool,
    description=generate_tool_description(
        name="Compute Expression",
        input_format="<a> <b> <c>",
        example_input="Compute 10 - 3 * 2",
        example_output="4"
    )
)
