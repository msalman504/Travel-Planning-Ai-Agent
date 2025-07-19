import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "travel-planning-agent")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    
    # Groq model configurations
    DEFAULT_MODEL = "llama3-70b-8192"  # or "mixtral-8x7b-32768", "gemma-7b-it"
    FALLBACK_MODEL = "llama3-8b-8192"  # Faster model for fallback
    
    @classmethod
    def setup_environment(cls):
        """Set up environment variables for LangChain and LangSmith."""
        os.environ["GROQ_API_KEY"] = cls.GROQ_API_KEY
        os.environ["LANGCHAIN_API_KEY"] = cls.LANGCHAIN_API_KEY
        os.environ["LANGCHAIN_TRACING_V2"] = cls.LANGCHAIN_TRACING_V2
        os.environ["LANGCHAIN_PROJECT"] = cls.LANGCHAIN_PROJECT
        
    @classmethod
    def validate_keys(cls):
        """Validate that all required API keys are present."""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required. Get it from https://console.groq.com/keys")
        if not cls.LANGCHAIN_API_KEY:
            raise ValueError("LANGCHAIN_API_KEY is required. Get it from https://smith.langchain.com/")