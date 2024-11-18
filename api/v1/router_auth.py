from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter(
    prefix="",
    tags=["Auth"]
)

templates = Jinja2Templates(directory=r"./templates")

@router.get("/auth", response_class=HTMLResponse)
async def get_auth(request: Request):

    return templates.TemplateResponse("auth.html", {"request": request})


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    
    user = request.session.get('login')

    if user:
        request.session.clear()  # Очистка сессии
        return templates.TemplateResponse("auth.html", {"request": request})
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    

def get_current_user(request: Request):
    """Проверка наличия активной сессии."""
    user = request.session.get("login")

    if not user:
        return None
    return user