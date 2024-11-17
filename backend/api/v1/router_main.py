from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from api.v1.router_auth import get_current_user
from pydantic import BaseModel

from db.session import DataBaseFilter, DataBaseCountIndex, DataBasePlan

router = APIRouter(
    prefix="",
    tags=["Main"]
)

db_filter = DataBaseFilter()
db_count = DataBaseCountIndex()
dbplan = DataBasePlan()

class ContentUpdateRequest(BaseModel):
    title: str

templates = Jinja2Templates(directory=r"./templates")

@router.get("/")
async def main_get(request: Request, user: dict = Depends(get_current_user)):
    
    if user:
        
        name_f = await db_filter.select_filter(user)
        
        if user == 35:
            username = 'Лёше'
        
        elif user == 807:
            username = 'Снеже'
        
        data_count_all = await db_count.select_count_all(username)
        count_plane = await dbplan.select_count_plan()
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "data_filter": name_f,
                "data_count_all_priority": data_count_all.count_priority,
                "data_count_all_user_name": data_count_all.count_user_name,
                "data_count_all_completion_date": data_count_all.count_completion_date,
                "data_count_all_checkbox_true": data_count_all.count_checkbox_true,
                "data_count_all_checkbox_false": data_count_all.count_checkbox_false,
                "data_count": count_plane
            }
        )
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    

@router.post("/update_content")
async def update_content_post(request: Request, data: ContentUpdateRequest):
    
    if data.title == 'Дом':
        return JSONResponse(content={
            'message': 'Content updated successfully',
            'data': '/home'
        })
    
    elif data.title == 'Покупки':
        return JSONResponse(content={
            'message': 'Content updated successfully',
            'data': '/store'
        })
    
    elif data.title == 'Учеба':
        return JSONResponse(content={
            'message': 'Content updated successfully',
            'data': '/study'
        })