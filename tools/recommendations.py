from langchain.agents import tool
from pydantic import BaseModel, Field
from typing import List
from langchain_core.tools import ToolException

class RecommendationInput(BaseModel):
    location: str = Field(description="City and country for recommendations")
    category: str = Field(description="Type: attractions, restaurants, or hotels")

@tool("destination_recommendations", args_schema=RecommendationInput)
def get_recommendations(location: str, category: str) -> str:
    """Get recommendations for attractions, restaurants, or hotels"""
    try:
        # Mock implementation
        recommendations = {
            "attractions": ["City Museum", "Historic District", "Botanical Gardens"],
            "restaurants": ["Local Cuisine Bistro", "Seafood Grill", "Rooftop Cafe"],
            "hotels": ["Grand Plaza Hotel", "Riverside Inn", "City Center Suites"]
        }
        
        return f"Top {category} in {location}:\n" + "\n".join(
            f"- {item}" for item in recommendations.get(category.lower(), [])
        )
    except Exception as e:
        raise ToolException(f"Recommendation error: {str(e)}")