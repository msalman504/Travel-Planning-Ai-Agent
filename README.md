# Groq-Powered Travel Planning Agent

A conversational AI assistant that helps you plan your travels using real-time weather, cost estimation, and destination recommendations. Powered by Groq LLMs, LangChain, and LangSmith for robust, traceable, and extensible agent workflows.

## Features
- **Weather Lookup:** Get current weather for any city.
- **Travel Cost Calculator:** Estimate travel costs between cities.
- **Destination Recommendations:** Find top attractions, restaurants, and hotels.
- **Fallback Handling:** If a tool fails, the agent gracefully switches to a fallback LLM response.
- **Interactive CLI:** Chat with the agent in your terminal.

## How It Works
- The agent uses [LangChain](https://github.com/langchain-ai/langchain) to orchestrate LLM calls and tool usage.
- Tools are defined as Python functions with Pydantic schemas and registered with LangChain's agent framework.
- [LangSmith](https://smith.langchain.com/) is used for tracing, debugging, and monitoring agent runs.
- The agent is powered by [Groq](https://groq.com/) LLMs for fast, high-quality responses.

## Setup & Usage
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/travel-planning-agent.git
   cd travel-planning-agent
   ```
2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in your API keys:
     - `GROQ_API_KEY` (from https://console.groq.com/keys)
     - `LANGCHAIN_API_KEY` (from https://smith.langchain.com/)
     - `WEATHER_API_KEY` (optional, for real weather data)

4. **Run the app:**
   ```bash
   python app.py
   ```
   - You'll enter an interactive chat session in your terminal.
   - Example queries:
     - `What's the weather like in Paris?`
     - `How much does it cost to fly from New York to London?`
     - `What are the top attractions in Tokyo?`

## How LangChain & LangSmith Help
- **LangChain** provides the agent framework, tool integration, and prompt management, making it easy to build complex, multi-step conversational agents.
- **LangSmith** enables tracing, debugging, and monitoring of agent runs, so you can see exactly how the agent makes decisions and diagnose issues quickly.

## Extending the Agent
- Add new tools in the `tools/` directory and register them in `agent/main_agent.py`.
- Modify the system prompt in `main_agent.py` to change the agent's behavior.
- Use LangSmith to trace and debug new workflows.

## License
MIT 