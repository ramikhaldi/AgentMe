import sys
import os
from flask import Flask, request, jsonify
from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, AgentType
from tools import discover_tools  # ✅ Auto-discover tools
from dotenv import load_dotenv

# ✅ Ensure Python can find `tools`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load environment variables
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")
TTYD_API_PORT = os.getenv("TTYD_API_PORT", "5000")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0"))  # ✅ Ensure float
OLLAMA_NUM_CTX = int(os.getenv("OLLAMA_NUM_CTX", "8000"))  # ✅ Ensure integer

app = Flask(__name__)

# ✅ 1️⃣ Connect to Ollama with temperature & context settings
llm = Ollama(
    model=MODEL_NAME,
    base_url="http://ollama:11434",
    temperature=OLLAMA_TEMPERATURE,  # ✅ Set temperature
    num_ctx=OLLAMA_NUM_CTX  # ✅ Set context length
)

# ✅ 2️⃣ Discover and load all available tools
custom_tools = discover_tools()
tool_names = {tool.name for tool in custom_tools}  # ✅ Store tool names for quick validation

# ✅ 3️⃣ Prepare tool descriptions for better LLM understanding
tool_descriptions = "\n".join([f"- {tool.name}: {tool.description}" for tool in custom_tools])

# ✅ 4️⃣ Initialize the agent with strict execution conditions
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
        # ✅ Step 1: Augment intent check with tool descriptions
        intent_prompt = (
            f"Below are the available tools:\n"
            f"{tool_descriptions}\n\n"
            f"Does the following request explicitly require using one of these tools?\n"
            f"Request: {user_input}\n\n"
            f"Respond with 'Yes' or 'No'."
        )
        print(f"intent_prompt: {intent_prompt}")
        intent_check = llm.invoke(intent_prompt).strip()
        print(f"intent_check: {intent_check}")

        if "No" in intent_check:
            print(f"\n🚨 [SECURITY]: User intent is unclear. Aborting execution.")
            return jsonify({"response": "I'm not sure what you're asking. Can you clarify?"})

        # ✅ Step 2: Invoke the agent
        response = agent.invoke({"input": user_input})
        print(f"response: {response}")

        found_final_answer = False
        for i, step in enumerate(response["intermediate_steps"]):
            action, observation = step  # Each step is (AgentAction, Observation)

            # ✅ Print all intermediate steps for debugging
            print(f"\n🔄 [INTERMEDIATE STEP {i+1}]")
            print(f"🛠️ Action: {action.tool}")
            print(f"📥 Input: {action.tool_input}")
            print(f"👀 Observation: {observation}")

            # ✅ Step 3: Reject execution if tool does not exist
            if action.tool not in tool_names:
                print(f"🚨 [SECURITY]: Unrecognized tool `{action.tool}` detected! Aborting execution.")
                return jsonify({"response": "I'm not sure what you're asking. Can you clarify?"})

            # ✅ Step 4: Return final result if found
            if "Final Answer:" in observation:
                final_result = observation.replace("Final Answer:", "").strip()
                print(f"\n🎯 [FINAL RESULT (found in intermediate steps)]: {final_result}")
                found_final_answer = True
                return jsonify({"response": final_result})

        # ✅ Step 5: If no final answer was found, print a warning and return output instead
        if not found_final_answer:
            print(f"\n⚠️ [WARNING]: No 'Final Answer' found in intermediate steps.")
            return jsonify({"response": response["output"]})

    except Exception as e:
        print(f"\n❌ [ERROR]: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print(f"🚀 Chatbot is starting... (Model: {MODEL_NAME}, Temperature: {OLLAMA_TEMPERATURE}, Context: {OLLAMA_NUM_CTX})")
    app.run(host="0.0.0.0", port=int(TTYD_API_PORT))
