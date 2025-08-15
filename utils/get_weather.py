import aiohttp

async def get_weather(city="Tashkent"):
    API_KEY = "a182e9ac096d5062c743b13932eb63a6"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"].capitalize()
            return f"{temp}°C, {description}"