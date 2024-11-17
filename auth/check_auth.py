from fastapi import Request, status, HTTPException

import ujson
import aiofiles


async def checking_user_entrance(login: int, password: str) -> dict:
    path = r"db/file_json/user_account.json"
    async with aiofiles.open(file=path, mode="r", encoding="utf-8") as file_json:
        
        file = ujson.loads(await file_json.read())
        dict_user = {}
        for k, v in file.items():

            if int(v['login']) == login:
                if v['password'] == password:
                    dict_user = {
                        'id': k,
                        'login': login,
                        'password': password
                    }
                break

        return dict_user