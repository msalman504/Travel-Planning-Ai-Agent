from langchain.agents import tool
from pydantic import BaseModel, Field
import random
from langchain_core.tools import ToolException

class CostInput(BaseModel):
    origin: str = Field(description="Origin city and country")
    destination: str = Field(description="Destination city and country")
    travel_class: str = Field(description="Economy, Business, First", default="Economy")

@tool("travel_cost_calculator", args_schema=CostInput)
def calculate_travel_cost(origin: str, destination: str, travel_class: str = "Economy") -> str:
    """Calculate approximate travel costs between locations"""
    try:
        # Mock implementation - replace with real API
        base_costs = {
            "Economy": 300,
            "Business": 800,
            "First": 1500
        }
        multiplier = random.uniform(0.8, 1.5)
        cost = base_costs.get(travel_class, 300) * multiplier
        
        return f"Estimated {travel_class} class travel from {origin} to {destination}: ${cost:.2f}"
    except Exception as e:
        raise ToolException(f"Cost calculation error: {str(e)}")