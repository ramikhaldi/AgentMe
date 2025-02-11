import os
import importlib.util
import inspect
from langchain_core.tools import Tool

def discover_tools():
    """Dynamically loads all tool modules inside `tools/`, including subdirectories."""
    tool_dir = os.path.dirname(__file__)  # Get directory of `tools/`
    valid_tools = []

    # ✅ Recursively find all Python files inside `tools/`
    for root, _, files in os.walk(tool_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_path = os.path.join(root, file)
                module_name = f"tools.{os.path.splitext(os.path.relpath(module_path, tool_dir))[0].replace(os.sep, '.')}"

                try:
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)  # ✅ Load module dynamically

                    # ✅ Extract all valid `Tool` objects from the module
                    for name, obj in inspect.getmembers(module):
                        if isinstance(obj, Tool):
                            valid_tools.append(obj)

                except Exception as e:
                    print(f"❌ [ERROR]: Failed to load `{module_name}` - {str(e)}")

    print(f"✅ [SANITY CHECK]: Found {len(valid_tools)} tool(s): {[t.name for t in valid_tools]}")
    return valid_tools  # ✅ Return list of discovered tools
