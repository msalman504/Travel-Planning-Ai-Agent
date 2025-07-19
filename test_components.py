from config import Config
from tools import get_weather, calculate_travel_cost, get_recommendations

def test_agent_components():
    """Test all agent components."""
    Config.setup_environment()
    
    print("Testing agent components...\n")
    
    # Test individual tools
    print("1. Testing Weather Tool:")
    weather_result = get_weather("London")
    print(f"   Result: {weather_result}")
    
    print("\n2. Testing Cost Calculator:")
    cost_result = calculate_travel_cost("New York", "Paris", "flight")
    print(f"   Result: {cost_result}")
    
    print("\n3. Testing Recommendations:")
    rec_result = get_recommendations("Tokyo", "attractions")
    print(f"   Result: {rec_result}")
    
    print("\n✅ All components tested successfully!")

if __name__ == "__main__":
    test_components()