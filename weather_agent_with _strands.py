from strands import Agent
from strands_tools import http_request

# Define a weather-focused system prompt
WEATHER_SYSTEM_PROMPT = """You are a weather assistant with HTTP capabilities. You can:

1. Make HTTP requests to the National Weather Service API
2. Process and display weather forecast data
3. Provide weather information for locations in the United States

When retrieving weather information:
1. First get the coordinates or grid information using https://api.weather.gov/points/{latitude},{longitude} or https://api.weather.gov/points/{zipcode}
2. Then use the returned forecast URL to get the actual forecast

When displaying responses:
- Format weather data in a human-readable way
- Highlight important information like temperature, precipitation, and alerts
- Handle errors appropriately
- Convert technical terms to user-friendly language

Always explain the weather conditions clearly and provide context for the forecast.
"""

# Create an agent with HTTP capabilities
weather_agent = Agent(
    system_prompt=WEATHER_SYSTEM_PROMPT,
    tools=[http_request],  # Explicitly enable http_request tool
)

# Let the agent handle the API details
response = weather_agent("What's the weather like in Seattle?")
response = weather_agent("Will it rain tomorrow in Miami?")
response = weather_agent("Compare the temperature in New York and Chicago this weekend")

# Direct API method calls with Strands
location_response = weather_agent.tool.http_request(
    method="GET",
    url="https://api.weather.gov/points/47.6062,-122.3321"  # Seattle coordinates
)

# Process response as needed
import json
location_data = json.loads(location_response['body'])
forecast_url = location_data.get('properties', {}).get('forecast')

# Make a second request to get the forecast
forecast_response = weather_agent.tool.http_request(
    method="GET",
    url=forecast_url
)