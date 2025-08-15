import aiohttp

async def get_quote():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://zenquotes.io/api/random") as resp:
            data = await resp.json()
            quote = data[0]["q"]
            author = data[0]["a"]
            return f'"{quote}" — {author}'
