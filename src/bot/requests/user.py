import aiohttp

from config import API_URL
from requests import post_request, get_request


async def create_user(chat_id: int, username: str = None, time_zone: str = "MSK+0"):
    user_data = {
        "chat_id": chat_id,
        "user_name": username,
        "time_zone": time_zone
    }
    response = await post_request('/api/user/', user_data)
    if type(response) == tuple:
        return response
    if response.status == 201:
        return True, "Пользователь успешно зарегистрирован!"
    elif response.status == 400:
        return True, "Пользователь уже существует"
    else:
        error_data = await response.json()
        return False, f"Ошибка: {error_data}"


async def get_user_by_chat_id(chat_id: int):
    response = await get_request(f'/api/user/by_chat_id/{chat_id}/')
    if type(response) == tuple:
        return response
    elif response.status == 200:
        return True, response.json()
    else:
        error_data = await response.json()
        return False, f"Ошибка: {error_data}"