from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import FileResponse

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

app = FastAPI(
    title='Доска Задач'
)

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
    
    dict_user = await checking_user_entrance(
        data.username,
        data.password
    )
    print(dict_user)
    if dict_user:
        request.session.update(dict_user)
        
        return JSONResponse(content={"message": "Успешная аутентификация"})
    else:
         
        raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")

 
@app.get("/favicon.ico")
async def favicon():
    return True
    return FileResponse("/static/pictures/favicon.ico")
