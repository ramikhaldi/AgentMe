# AgentMe

🚀 **Empower Your AI Assistant with Custom Logic and Action Execution!** 🚀

AgentMe is an agentic AI solution that enables you to **command your local AI Agent to execute predefined actions using a usual discussion with your chatbot**. Unlike traditional chatbot solutions, AgentMe provides seamless **privacy-focused** interactions—your queries and executions remain within your environment, ensuring **maximum privacy and security**.

### 🛡️ **Run Local AI on Your Machine with Full Control**

Unlike cloud-based AI solutions that may expose your data to external servers, **AgentMe runs entirely on your local machine**. This means:

- ✅ **No data leakage**—all interactions stay private.
- ✅ **Customizable & Extendable**—modify or add tools to match your needs.
- ✅ **Performance Optimized**—local execution ensures low latency and high responsiveness.

With AgentMe, you can integrate your **own logic**, making your AI assistant as powerful and flexible as you need. Define your own tools, automate tasks, and process information efficiently—all with simple Python functions!

## 🚀 Features

- **LLM-Powered:** Uses **Ollama** for natural language processing.
- **Dynamic Tool Discovery:** Custom tool functions can be added under `chatbot/tools/` as separate Python files.
- **Secure Execution:** Prevents unauthorized tool usage with similarity checks.
- **Containerized & Highly Portable:** Runs seamlessly across different environments with easy deployment.
- **Automatic Model Loading:** Ensures the required model is preloaded before execution.
- **Unmatched Customization:** Create your own tools and logic to extend the agent’s functionality!

## 🛠️ Prerequisites

### 🖥️ **For Windows Users**

- Install **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**
- Ensure **WSL 2 backend** is enabled (recommended for performance)
- Make sure **Linux Containers** are enabled

### 🐧 **For Linux Users**

- Install **Docker Engine** ([Guide](https://docs.docker.com/engine/install/))
- Install **Docker Compose** ([Guide](https://docs.docker.com/compose/install/))

## 📦 Installation & Setup

### 1️⃣ Clone the Repository

```sh
$ git clone https://github.com/ramikhaldi/AgentMe.git
$ cd AgentMe
```

### 2️⃣ Start the Application

#### **Windows**

Run `start.bat`:

```sh
$ start.bat
```

#### **Linux/macOS**

Run `start.sh`:

```sh
$ chmod +x start.sh
$ ./start.sh
```

This **automatically performs a comprehensive sanity check**, verifying:
- ✅ **Docker & Docker Compose**
- ✅ **NVIDIA GPU support & containerization**

If any issue is detected, the script will provide **clear guidance on how to fix it**.

---

## ⚙️ Configurable Parameters

AgentMe allows fine-tuning via environment variables in the .env file:

| Parameter            | Default Value | Description                                                 |
| -------------------- | ------------- | ----------------------------------------------------------- |
| `MODEL_NAME`         | `llama3.2:3b` | Specifies the LLM model used.                               |
| `AGENTME_API_PORT`   | `5000`        | Port where the chatbot API runs.                            |
| `OLLAMA_TEMPERATURE` | `0.0`         | Controls randomness in responses (higher is more creative). |
| `OLLAMA_NUM_CTX`     | `8000`        | Sets the maximum context window size.                       |

## 📌 Usage

### 🔹 **Sending a Request to AgentMe**

You can interact with the chatbot via a simple **cURL** request:

```sh
curl -v -X POST "http://localhost:5000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "give me fib of 10"}'
```

#### ✅ Expected Response:

```json
{"response":"55"}
```

## 🛠️ Custom Tool Functions

You can add custom Python tools under `chatbot/tools/` as separate files. Each file must implement a callable function that returns a result.

### 🧩 **Example: Defining Custom Logic**

Your custom tools can **do whatever you want!** Make sure they are well documented so the action can be recognized.

#### Example: **Fibonacci Calculator (chatbot/tools/fibonacci.py)**

```python
from langchain_core.tools import Tool
from utils import generate_tool_description

def fibonacci(n):
    """Calculates the Fibonacci sequence for a given number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def run_fibonacci_tool(n):
    """Wrapper function for LangChain"""
    result = fibonacci(int(n))
    return f"Final Answer: {result}"

fibonacci_tool = Tool(
    name="Fibonacci Calculator",
    func=run_fibonacci_tool,
    description=f"Call this tool if a Fibonacci of number has to be computed. Use 'Action: Fibonacci Calculator' and pass the input as 'Action Input: <number>'.\n"
)
```

This tool will be **automatically discovered** by AgentMe and made available for execution!

## 🛠️ Development & Contribution

TTYD is **open-source**, and contributions are welcome! 🎉

### 🔨 **Local Development**

1. Fork & clone the repo.
2. Modify/extend/Improve.
3. Run, Test, and benchmark.
4. Submit a pull request. 🚀

## 📜 License

This project is licensed under the **MIT License**.

---

Enjoy using **AgentMe** and contribute to its development! 🎉

