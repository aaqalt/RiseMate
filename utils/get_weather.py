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

async def get_weather(lat: float = None, lon: float = None, location_name: str = None):
    if not ((lat is not None and lon is not None) or location_name):
        return None, None  # nothing to fetch

    async with aiohttp.ClientSession() as session:
        if lat is not None and lon is not None:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
        else:
            loc = location_name.replace(" ", "+")
            url = f"https://api.openweathermap.org/data/2.5/weather?q={loc}&units=metric&appid={API_KEY}"

        try:
            async with session.get(url) as resp:
                data = await resp.json()
                if resp.status != 200 or "main" not in data:
                    return None, None
        except Exception:
            return None, None

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        main_weather = data["weather"][0]["main"]
        description = WEATHER_EMOJIS.get(main_weather, main_weather)

        city = data.get("name", "")
        country = data.get("sys", {}).get("country", "")
        location_name_resp = f"{city}, {country}" if city and country else city or "Unknown location"

        weather_text = f"{location_name_resp}: {description}, 🌡 {temp}°C (feels like {feels_like}°C)"
        return weather_text, location_name_resp
