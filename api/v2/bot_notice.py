from core.config import config

import requests

API_URL = 'https://api.telegram.org/bot'

async def send_message_home_add(chat_id, type_t, text, username):
    
    message = f'{API_URL}{config.BOT_TOKEN.get_secret_value()}/sendMessage?chat_id={chat_id}&text=Дом\n\nТип: {type_t}\nЗадача: {text}\nНазначено: {username}'
    requests.get(message)
    
    return True


async def send_message_store_add(chat_id, type_t, text, username):
    
    message = f'{API_URL}{config.BOT_TOKEN.get_secret_value()}/sendMessage?chat_id={chat_id}&text=Покупки\n\nТип: {type_t}\nЗадача: {text}\nИзменения: {username}'
    requests.get(message)
    
    return True


async def send_message_home_update(chat_id, text, event):
    
    message = f'{API_URL}{config.BOT_TOKEN.get_secret_value()}/sendMessage?chat_id={chat_id}&text=Дом\n\nЗадача: {text}\nИзменения: {event}'
    requests.get(message)
    
    return True


async def send_message_store_update(chat_id, text, event):
    
    message = f'{API_URL}{config.BOT_TOKEN.get_secret_value()}/sendMessage?chat_id={chat_id}&text=Покупки\n\nЗадача: {text}\nИзменения: {event}'
    requests.get(message)
    
    return True