import os
import requests
from agents import function_tool
from dotenv import load_dotenv

load_dotenv()

@function_tool
async def fetch_weather(city: str) -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise ValueError("WEATHER_API_KEY is not set. Please check your .env file.")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data.get("cod") == 200:
        main = data["main"]
        weather = data["weather"][0]["description"]
        return f"Weather in {city}: {weather}, Temperature: {main['temp']}°C"
    else:
        return "City not found."
