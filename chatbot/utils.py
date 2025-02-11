import sys
import importlib
import inspect
from langchain_community.tools import Tool

def check_custom_tools():
    """Find and validate all tools in `tools.tools`."""
    try:
        tools_module = importlib.import_module("tools.tools")
        print("✅ [SANITY CHECK]: `tools.tools` loaded successfully.")

        valid_tools = []
        for name, obj in inspect.getmembers(tools_module):
            if isinstance(obj, Tool):
                valid_tools.append(obj)

        if not valid_tools:
            raise ValueError("❌ [ERROR]: No valid LangChain `Tool` found in `tools.tools`.")

        print(f"✅ [SANITY CHECK]: Found {len(valid_tools)} tool(s): {[t.name for t in valid_tools]}")
        return valid_tools  # ✅ Return tool list instead of forcing prompt changes

    except Exception as e:
        print(f"❌ [ERROR]: Failed to load `tools.tools` - {str(e)}")
        sys.exit(1)


def generate_tool_description(name, input_format, example_input, example_output):
    """
    Dynamically generates a standardized tool description for LangChain.
    
    Args:
    - name: The tool name (string).
    - input_format: Expected input format (string), e.g., "<a> <b> <c>"
    
    Returns:
    - A formatted description string.
    """
    return (
        f"Call this tool using 'Action: {name}' and pass the input as 'Action Input: {input_format}'.\n"
    )