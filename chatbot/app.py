import sys
import os
from flask import Flask, request, jsonify
from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, AgentType
from tools import discover_tools  # ✅ Load all tools automatically
from dotenv import load_dotenv

# ✅ Ensure Python can find `tools`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load environment variables
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")
TTYD_API_PORT = os.getenv("TTYD_API_PORT", "5000")

app = Flask(__name__)

# ✅ 1️⃣ Connect to Ollama (running in Docker network)
llm = Ollama(model=MODEL_NAME, base_url="http://ollama:11434")

# ✅ 2️⃣ Dynamically load all tools
custom_tools = discover_tools()

# ✅ 3️⃣ Initialize the agent
agent = initialize_agent(
    custom_tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=2,
    return_intermediate_steps=True,
    handle_parsing_errors=True
)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    print(f"\n📥 [USER QUESTION]: {user_input}")

    try:
        # ✅ Use `invoke()` instead of `run()`
        response = agent.invoke({"input": user_input})

        # ✅ Extract the correct final answer from `intermediate_steps`
        found_final_answer = False
        for i, step in enumerate(response["intermediate_steps"]):
            action, observation = step  # Each step is (AgentAction, Observation)

            # ✅ Print all intermediate steps for debugging
            print(f"\n🔄 [INTERMEDIATE STEP {i+1}]")
            print(f"🛠️ Action: {action.tool}")
            print(f"📥 Input: {action.tool_input}")
            print(f"👀 Observation: {observation}")

            # ✅ Check for "Final Answer:"
            if "Final Answer:" in observation:
                final_result = observation.replace("Final Answer:", "").strip()
                print(f"\n🎯 [FINAL RESULT (found in intermediate steps)]: {final_result}")
                found_final_answer = True
                return jsonify({"response": final_result})

        # ✅ If no final answer was found, print a warning and return output instead
        if not found_final_answer:
            print(f"\n⚠️ [WARNING]: No 'Final Answer' found in intermediate steps.")
            return jsonify({"response": response["output"]})

    except Exception as e:
        print(f"\n❌ [ERROR]: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 AgentMe Server is starting...")
    app.run(host="0.0.0.0", port=int(TTYD_API_PORT))
