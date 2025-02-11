import sys
import os
from flask import Flask, request, jsonify
from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, AgentType
from tools import discover_tools  # ✅ Auto-discover tools
from dotenv import load_dotenv
from rapidfuzz import process

# ✅ Ensure Python can find `tools`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load environment variables
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME")
AGENTME_API_PORT = os.getenv("AGENTME_API_PORT")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE"))
OLLAMA_NUM_CTX = int(os.getenv("OLLAMA_NUM_CTX"))

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
    max_iterations=1,
    return_intermediate_steps=True,
    handle_parsing_errors=True,
    memory=None,  # ✅ Ensure NO memory is retained
    early_stopping_method="generate"  # ✅ Stop after generating a final answer
)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    print(f"\n📥 [USER QUESTION]: {user_input}")

    try:
        # ✅ Reset memory to prevent state retention
        agent.memory = None

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

        for i, step in enumerate(response["intermediate_steps"]):
            action, observation = step

            print(f"\n🔄 [INTERMEDIATE STEP {i+1}]")
            print(f"🛠️ Action: {action.tool}")
            print(f"📥 Input: {action.tool_input}")
            print(f"👀 Observation: {observation}")

            # ✅ Find the best tool match (case-insensitive + semantic similarity)
            best_match, score, _ = process.extractOne(action.tool, tool_names)

            if score < 80:
                print(f"🚨 [SECURITY]: Unrecognized tool `{action.tool}` detected! Closest match `{best_match}` (score: {score}). Aborting execution.")
                return jsonify({"response": "I'm not sure what you're asking. Can you clarify?"})

            print(f"✅ [MATCH]: Using `{best_match}` instead of `{action.tool}` (Similarity: {score}%)")
            action.tool = best_match

            # ✅ Step 3: Stop execution **immediately** after finding "Final Answer"
            if "Final Answer:" in observation:
                final_result = observation.replace("Final Answer:", "").strip()
                print(f"\n🎯 [FINAL RESULT]: {final_result}")

                # 🔥 **Force agent to stop execution early**
                return jsonify({"response": final_result})

        # ✅ Step 4: If no final answer was found, return raw output
        print(f"\n⚠️ [WARNING]: No 'Final Answer' found in intermediate steps.")
        return jsonify({"response": response["output"]})

    except Exception as e:
        print(f"\n❌ [ERROR]: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print(f"🚀 Chatbot is starting... (Model: {MODEL_NAME}, Temperature: {OLLAMA_TEMPERATURE}, Context: {OLLAMA_NUM_CTX})")
    app.run(host="0.0.0.0", port=int(AGENTME_API_PORT))
