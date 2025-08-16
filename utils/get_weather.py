import aiohttp 

API_KEY = "a182e9ac096d5062c743b13932eb63a6"

WEATHER_EMOJIS = {
    "Clear": "☀️ Sunny",
    "Clouds": "☁️ Cloudy",
    "Rain": "🌧 Rainy",
    "Drizzle": "🌦 Drizzle",
    "Thunderstorm": "⛈ Thunderstorm",
    "Snow": "❄️ Snowy",
    "Mist": "🌫 Misty",
    "Fog": "🌫 Foggy"
}

async def get_weather(lat: float, lon: float):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
        async with session.get(url) as resp:
            data = await resp.json()
            if resp.status != 200 or "main" not in data:
                return None, None  

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        main_weather = data["weather"][0]["main"]  # e.g., "Clear", "Clouds"
        description = WEATHER_EMOJIS.get(main_weather, main_weather)  # fallback to text

        city = data.get("name", "")
        country = data.get("sys", {}).get("country", "")
        location_name = f"{city}, {country}" if city and country else city or "Unknown location"

        weather_text = f"{location_name}: {description}, 🌡 {temp}°C (feels like {feels_like}°C)"
        return weather_text, location_name
