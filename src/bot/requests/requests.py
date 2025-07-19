import aiohttp

from config import API_URL


async def get_request(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{API_URL}{url}') as response:
                return response
    except Exception as e:
        return False, f"Ошибка соединения: {str(e)}"


async def post_request(url: str, request_body: dict):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{API_URL}{url}', json=request_body) as response:
                return response
    except Exception as e:
        return False, f"Ошибка соединения: {str(e)}"
