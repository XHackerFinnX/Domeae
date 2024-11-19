from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from api.v1.router_auth import get_current_user
from pydantic import BaseModel

from db.session import DataBaseFilter


router = APIRouter(
    prefix="",
    tags=["Filter"]
)

db_filter = DataBaseFilter()

class ContentUpdateRequest(BaseModel):
    title: str
    
class OptionFilter(BaseModel):
    option: str
    
class OptionFilterCompleted(BaseModel):
    option: str
    name: str
    
templates = Jinja2Templates(directory=r"./templates")

@router.post("/filter")
async def filter_post(request: Request, option_v: OptionFilter, user: dict = Depends(get_current_user)):
    
    data_f = None
    if user:
        
        if option_v.option == 'today':
            data_f = 'today'
        
        elif option_v.option == 'priority':
            data_f = 'priority'
        
        elif option_v.option == 'user':
            data_f = 'user'
        
        await db_filter.update_filter(user, data_f)
        
        return JSONResponse(content={
                'message': 'filter ok',
                'data': '/'
            })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    

@router.post("/filter_delete")
async def filter_delete_post(request: Request, option_v: OptionFilter, user: dict = Depends(get_current_user)):
    
    if user:
        
        await db_filter.update_filter(user, None)
        
        return JSONResponse(content={
                'message': 'filter ok',
                'data': '/'
            })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    

@router.post("/filter_completed")
async def filter_completed_post(request: Request, option_c: OptionFilterCompleted, user: dict = Depends(get_current_user)):
    
    if user:
        
        return JSONResponse(content={
                'message': 'completed ok',
                'data': f'/completed?name={option_c.name}'
            })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})