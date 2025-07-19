from langchain.agents import AgentExecutor
from langchain_groq import ChatGroq
from config import Config

class FallbackAgent:
    def __init__(self, primary_agent: AgentExecutor):
        self.primary_agent = primary_agent
        # Use a faster Groq model for fallback
        self.fallback_llm = ChatGroq(
            model=Config.FALLBACK_MODEL,
            temperature=0.3,
            max_tokens=512,
            timeout=30
        )
    
    def run_with_fallback(self, query: str) -> str:
        """Run the primary agent with fallback handling."""
        try:
            # Try primary agent first
            print("🤖 Using Groq-powered agent with tools...")
            result = self.primary_agent.invoke({"input": query})
            return result["output"]
        
        except Exception as e:
            print(f"⚠️  Primary agent failed: {str(e)}")
            print("🔄 Switching to fallback mode...")
            
            # Fallback to simple LLM response
            fallback_prompt = f"""You are a helpful travel assistant. I'm experiencing technical difficulties with my travel planning tools, but I can still provide general travel advice.

User question: {query}

Please provide a helpful response about travel planning. Be concise but informative. If the question requires specific real-time data (like current weather or exact prices), acknowledge that you cannot provide that information due to technical issues, but offer general guidance instead."""
            
            try:
                fallback_response = self.fallback_llm.invoke(fallback_prompt)
                return f"[Fallback Mode - Groq Direct] {fallback_response.content}"
            except Exception as fallback_error:
                return f"I apologize, but I'm currently experiencing technical difficulties with both my tools and fallback systems. Please try again later. Error: {str(fallback_error)}"
    
    def test_connection(self) -> bool:
        """Test if Groq connection is working."""
        try:
            test_response = self.fallback_llm.invoke("Say 'Connection successful' if you can read this.")
            return "successful" in test_response.content.lower()
        except Exception:
            return False