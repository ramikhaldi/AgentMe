import sys
import os

# ✅ Add `/app` so Python can find `custom_logic`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, jsonify
from langchain_community.llms import Ollama
from langchain_community.tools import Tool
from langchain_community.agent_toolkits import load_tools
from langchain.agents import initialize_agent
from dotenv import load_dotenv
from custom_logic.tools import fibonacci_tool  # ✅ Now Python should find this!

# Load environment variables from .env
load_dotenv()

# Get variables from .env
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")
TTYD_API_PORT = os.getenv("TTYD_API_PORT", "5000")

app = Flask(__name__)

# ✅ 1️⃣ Connect to Ollama (running in Docker network)
llm = Ollama(model=MODEL_NAME, base_url="http://ollama:11434")

# ✅ 2️⃣ Manually create tools instead of using `load_tools()`
tools = [
    fibonacci_tool      # Custom logic
]

# ✅ 3️⃣ Initialize LangChain Agent
agent = initialize_agent(tools, llm, agent="zero-shot-react-description")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    # ✅ Let LangChain decide execution method
    response = agent.run(user_input)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
