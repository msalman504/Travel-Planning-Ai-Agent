from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage
from langchain.callbacks import LangChainTracer
from langchain.callbacks.manager import CallbackManager

from tools import get_weather, calculate_travel_cost, get_recommendations
from config import Config


class TravelAgent:
    """Main travel planning agent class using Groq."""

    def __init__(self, model=None, temperature=0.7, max_tokens=1024, verbose=True):
        """
        Initialize the travel agent.
        Args:
            model (str): Model to use (defaults to Config.DEFAULT_MODEL)
            temperature (float): Sampling temperature
            max_tokens (int): Maximum tokens for responses
            verbose (bool): Enable verbose logging
        """
        self.model = model or Config.DEFAULT_MODEL
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.verbose = verbose

        # Initialize tools
        self.tools = [get_weather, calculate_travel_cost, get_recommendations]

        # Create callback manager for tracing
        self.callback_manager = CallbackManager([LangChainTracer()])

        # Initialize the agent executor
        self.agent_executor = self._create_agent()

    def _create_agent(self):
        """Create and configure the agent executor."""

        # Initialize the Groq LLM
        llm = ChatGroq(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=60,
            max_retries=2,
            callbacks=[LangChainTracer()]
        )

        # Create agent prompt (optimized for Groq models)
        system_message = """You are a helpful travel planning assistant powered by Groq. You can help users with:
        1. Weather information for destinations
        2. Travel cost calculations  
        3. Destination recommendations (attractions, restaurants, hotels)

        Instructions:
        - Be friendly and provide comprehensive travel advice
        - Use the available tools to get accurate information
        - If you encounter errors, acknowledge them and suggest alternatives
        - Ask for clarification if the user's request is ambiguous
        - Provide context and helpful additional information
        - Suggest related services when appropriate
        - Keep responses concise but informative

        Available tools:
        - weather_lookup: Get current weather for any city
        - travel_cost_calculator: Calculate travel costs between cities
        - destination_recommendations: Get recommendations for attractions, restaurants, or hotels
        """

        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_message),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        # Create the agent (using tool calling for Groq)
        agent = create_tool_calling_agent(
            llm=llm,
            tools=self.tools,
            prompt=prompt
        )

        # Create agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            callback_manager=self.callback_manager,
            verbose=self.verbose,
            handle_parsing_errors=True,
            max_iterations=5,
            early_stopping_method="generate"
        )

        return agent_executor

    def invoke(self, input_text, chat_history=None):
        """
        Process user input and return agent response.
        Args:
            input_text (str): User's travel query
            chat_history (list): Optional chat history
        Returns:
            dict: Agent response with output and metadata
        """
        inputs = {"input": input_text}
        if chat_history:
            inputs["chat_history"] = chat_history

        return self.agent_executor.invoke(inputs)

    def stream(self, input_text, chat_history=None):
        """
        Stream agent response for real-time interaction.
        Args:
            input_text (str): User's travel query
            chat_history (list): Optional chat history
        Yields:
            dict: Streaming response chunks
        """
        inputs = {"input": input_text}
        if chat_history:
            inputs["chat_history"] = chat_history

        for chunk in self.agent_executor.stream(inputs):
            yield chunk

    async def ainvoke(self, input_text, chat_history=None):
        """
        Asynchronously process user input.
        Args:
            input_text (str): User's travel query
            chat_history (list): Optional chat history
        Returns:
            dict: Agent response with output and metadata
        """
        inputs = {"input": input_text}
        if chat_history:
            inputs["chat_history"] = chat_history

        return await self.agent_executor.ainvoke(inputs)

    def get_tools(self):
        """Return list of available tools."""
        return self.tools

    def update_config(self, **kwargs):
        """
        Update agent configuration and recreate agent.
        Args:
            **kwargs: Configuration parameters to update
        """
        if 'model' in kwargs:
            self.model = kwargs['model']
        if 'temperature' in kwargs:
            self.temperature = kwargs['temperature']
        if 'max_tokens' in kwargs:
            self.max_tokens = kwargs['max_tokens']
        if 'verbose' in kwargs:
            self.verbose = kwargs['verbose']

        # Recreate agent with new configuration
        self.agent_executor = self._create_agent()

    def get_config(self):
        """Return current agent configuration."""
        return {
            'model': self.model,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'verbose': self.verbose
        }


# For backward compatibility, you can still create an instance easily
def create_travel_agent(**kwargs):
    """Factory function to create a TravelAgent instance."""
    return TravelAgent(**kwargs)
