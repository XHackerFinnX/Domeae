import re
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from auth.check_auth import checking_user_entrance
from api.v1.router_main import router as router_main
from api.v1.router_auth import router as router_auth
from api.v1.router_home import router as router_home
from api.v1.router_store import router as router_store
from api.v1.router_study import router as router_study
from api.v1.router_plan import router as router_plan
from api.v1.router_filter import router as router_filter
from api.v1.router_complet import router as router_complet
from api.v1.router_launcher import router as router_launcher
from api.v1.router_enemies import router as router_enemies

from core.config import config

# ---------------------- WAF Middleware ----------------------
class SimpleWAFMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.blocked_patterns = [
            re.compile(r"\.env", re.IGNORECASE),
            re.compile(r"\.php", re.IGNORECASE),
            re.compile(r"\.git", re.IGNORECASE),
            re.compile(r"\.svn", re.IGNORECASE),
            re.compile(r"\.bak", re.IGNORECASE),
            re.compile(r"phpinfo", re.IGNORECASE),
            re.compile(r"debug", re.IGNORECASE),
            re.compile(r"config", re.IGNORECASE),
            re.compile(r"db\.json", re.IGNORECASE),
            re.compile(r"deployment-config", re.IGNORECASE),
            re.compile(r"live_env", re.IGNORECASE),
            re.compile(r"restore", re.IGNORECASE),
            re.compile(r"robomongo", re.IGNORECASE),
        ]

    async def dispatch(self, request: Request, call_next):
        path = str(request.url.path)
        for pattern in self.blocked_patterns:
            if pattern.search(path):
                return Response("🚫 Запрос заблокирован WAF", status_code=403)
        return await call_next(request)

# ------------------------------------------------------------

app = FastAPI(title='Доска Задач')

# WAF должен быть добавлен самым первым
app.add_middleware(SimpleWAFMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    r"/static",
    StaticFiles(directory='static'),
    name="static"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=config.SECRET_AUTH.get_secret_value(),
    session_cookie="session",
    max_age=2000000
)

# Подключение роутеров
app.include_router(router_auth)
app.include_router(router_main)
app.include_router(router_home)
app.include_router(router_store)
app.include_router(router_study)
app.include_router(router_plan)
app.include_router(router_filter)
app.include_router(router_complet)
app.include_router(router_launcher)
app.include_router(router_enemies)

class LoginData(BaseModel):
    username: int
    password: str

@app.post('/login')
async def post_login(request: Request, data: LoginData):
    print(data)
    dict_user = await checking_user_entrance(data.username, data.password)
    print(dict_user)
    if dict_user:
        request.session.update(dict_user)
        return JSONResponse(content={"message": "Успешная аутентификация"})
    else:
        raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("/static/pictures/favicon.ico")