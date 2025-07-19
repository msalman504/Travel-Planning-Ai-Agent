import sys

import logging

from config import Config

from agent import TravelAgent, FallbackAgent, TravelPlanningWorkflow

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class TravelPlanningApp:

    def __init__(self):

        try:

            # Validate configuration

            Config.validate_keys()

            Config.setup_environment()

            

            print("🚀 Initializing Groq-powered Travel Planning Agent...")

            

            # Initialize components

            logger.info("🚀 Initializing Groq-powered Travel Planning Agent...")

            agent_executor = TravelAgent()

            self.agent = FallbackAgent(agent_executor)

            self.workflow = TravelPlanningWorkflow()

            

            # Test connection

            if self.agent.test_connection():

                print("✅ Groq connection successful!")

            else:

                print("⚠️  Groq connection test failed, but continuing...")

                

        except ValueError as e:

            print(f"❌ Configuration error: {e}")

            sys.exit(1)

        except Exception as e:

            print(f"❌ Initialization error: {e}")

            sys.exit(1)

    

    def run_interactive_session(self):

        """Run an interactive travel planning session."""

        print("\n🌍 Welcome to the Groq-Powered Travel Planning Assistant!")

        print("I can help you with weather, costs, and recommendations for your trip.")

        print("Powered by Groq's fast inference and LangChain's agent framework.")

        print("Type 'quit' to exit, 'help' for commands.\n")

        

        while True:

            user_input = input("User: ").strip()

            

            if user_input.lower() in ['quit', 'exit', 'bye']:

                print("Travel Agent: Safe travels! Goodbye! 👋")

                break

            

            if user_input.lower() == 'help':

                self.show_help()

                continue

            

            if not user_input:

                continue

            

            try:

                response = self.agent.run_with_fallback(user_input)

                print(f"Travel Agent: {response}\n")

                

            except Exception as e:

                print(f"Travel Agent: I apologize for the error: {str(e)}\n")

    

    def show_help(self):

        """Show available commands and examples."""

        help_text = """

Available commands:

- 'quit' or 'exit': Exit the application

- 'help': Show this help message



Example queries:

- "What's the weather like in Paris?"

- "How much does it cost to fly from New York to London?"

- "What are the top attractions in Tokyo?"

- "Plan a trip to Rome with weather, costs, and recommendations"

- "I need restaurant recommendations for Barcelona"



The agent can combine multiple requests in one query!

        """

        print(help_text)

    

    def run_single_query(self, query: str):

        """Run a single query."""

        print(f"🔍 Query: {query}")

        response = self.agent.run_with_fallback(query)

        print(f"🤖 Response: {response}\n")

        return response

    

    def run_structured_workflow(self, user_input: str):

        """Run the structured workflow."""

        print("🔄 Running structured travel planning workflow...")

        

        context = {"user_input": user_input}

        result = self.workflow.run(context)

        

        print("📋 Workflow Results:")

        print(result.get("final_summary", "Workflow completed"))

        

        return result

    

    def run_batch_queries(self, queries: list):

        """Run multiple queries in batch."""

        print("🔄 Running batch queries...")

        results = []

        

        for i, query in enumerate(queries, 1):

            print(f"\n--- Query {i}/{len(queries)} ---")

            result = self.run_single_query(query)

            results.append(result)

        

        return results

if __name__ == "__main__":
    app = TravelPlanningApp()
    app.run_interactive_session()