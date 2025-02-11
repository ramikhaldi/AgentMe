import sys
import importlib
import inspect
from langchain_community.tools import Tool

def check_custom_tools():
    """Find and validate all tools in `custom_logic.tools`."""
    try:
        tools_module = importlib.import_module("custom_logic.tools")
        print("✅ [SANITY CHECK]: `custom_logic.tools` loaded successfully.")

        valid_tools = []
        for name, obj in inspect.getmembers(tools_module):
            if isinstance(obj, Tool):
                valid_tools.append(obj)

        if not valid_tools:
            raise ValueError("❌ [ERROR]: No valid LangChain `Tool` found in `custom_logic.tools`.")

        print(f"✅ [SANITY CHECK]: Found {len(valid_tools)} tool(s): {[t.name for t in valid_tools]}")
        return valid_tools  # ✅ Return tool list instead of forcing prompt changes

    except Exception as e:
        print(f"❌ [ERROR]: Failed to load `custom_logic.tools` - {str(e)}")
        sys.exit(1)


def generate_tool_description(name, input_format, example_input, example_output):
    """
    Dynamically generates a standardized tool description for LangChain.
    
    Args:
    - name: The tool name (string).
    - input_format: Expected input format (string).
    - example_input: Example input value (string).
    - example_output: Example output value (string).
    
    Returns:
    - A formatted description string.
    """
    return (
        f"Use this tool to perform a specific task.\n"
        f"Call this tool using 'Action: {name}' and pass the input as 'Action Input: {input_format}'.\n"
        f"Example usage:\n"
        f"Question: {example_input}\n"
        f"Thought: I should use {name}.\n"
        f"Action: {name}\n"
        f"Action Input: {input_format}\n"
        f"Observation: Final Answer: {example_output}\n"
        f"The agent must stop after seeing 'Final Answer:'."
    )