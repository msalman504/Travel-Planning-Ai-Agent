from langchain.agents import tool
from pydantic import BaseModel, Field
import random
from typing import Optional
import requests
from config import Config
from langchain_core.tools import ToolException

class WeatherInput(BaseModel):
    city: str = Field(description="The city name to get weather for")
    country: str = Field(description="The country code (optional)", default="")

@tool("weather_lookup", args_schema=WeatherInput)
def get_weather(city: str, country: str = "") -> str:
    """Get current weather information for a specific city."""
    try:
        # If you have a real weather API key, use this:
        if Config.WEATHER_API_KEY and Config.WEATHER_API_KEY != "your_weather_api_key_here":
            return get_real_weather(city, country)
        
        # Mock weather API call for demo
        weather_conditions = [
            "sunny and clear", "partly cloudy", "overcast", 
            "light rain", "heavy rain", "thunderstorms",
            "snow", "foggy", "windy"
        ]
        temp = random.randint(5, 35)
        condition = random.choice(weather_conditions)
        humidity = random.randint(30, 90)
        
        return f"Weather in {city}: {condition}, {temp}°C, {humidity}% humidity. Perfect for exploring the city!"
    except Exception as e:
        raise ToolException(f"Unable to fetch weather for {city}. Error: {str(e)}. Please try again later.")

def get_real_weather(city: str, country: str = "") -> str:
    """Get real weather data from OpenWeatherMap API."""
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        location = f"{city},{country}" if country else city
        
        params = {
            "q": location,
            "appid": Config.WEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        
        return f"Current weather in {city}: {weather}, {temp}°C, {humidity}% humidity"
    except Exception as e:
        raise ToolException(f"Unable to fetch real weather data for {city}: {str(e)}") 