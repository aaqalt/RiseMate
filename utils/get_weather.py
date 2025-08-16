import aiohttp 

import os

API_KEY = os.getenv("a182e9ac096d5062c743b13932eb63a6")

async def get_weather(lat: float, lon: float):
    async with aiohttp.ClientSession() as session:
        # Get weather by lat/lon
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
        async with session.get(url) as resp:
            data = await resp.json()
            if resp.status != 200 or "main" not in data:
                return None, None  

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"].capitalize()

        # Get location name (city)
        city = data.get("name", "")
        country = data.get("sys", {}).get("country", "")
        location_name = f"{city}, {country}" if city and country else city or "Unknown location"

        weather_text = f"{location_name}: {description}, 🌡 {temp}°C (feels like {feels_like}°C)"
        return weather_text, location_name