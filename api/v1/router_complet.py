from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from typing import Annotated, Literal

from api.v1.router_auth import get_current_user
from pydantic import BaseModel

from db.session import DataBaseCountIndex, DataBasePlan, DataBaseHome, DataBaseStory, DataBaseCompleted

router = APIRouter(
    prefix="",
    tags=["Completed"]
)

db_count = DataBaseCountIndex()
dbplan = DataBasePlan()
dbhome = DataBaseHome()
dbstore = DataBaseStory()
dbcomp = DataBaseCompleted()

class ContentUpdateRequest(BaseModel):
    title: str
    
class DeletComplet(BaseModel):
    pcontent: str
    sassigned: str
    sprice: str
    

class DeleteSelectedCompleted(BaseModel):
    tasks: list

    
templates = Jinja2Templates(directory=r"./templates")


@router.get("/completed")
async def completed_name_get(request: Request, name: str = Literal["all", "home", "store"], user: dict = Depends(get_current_user)):
    
    if user:
        
        if user == 35:
            username = 'Лёше'
            
        elif user == 807:
            username = 'Снеже'
            
        
        if name == 'all':
            data_count_completion_date = await db_count.select_count_all(username)
            data_completed = await dbcomp.completed_home() + await dbcomp.completed_store()
        
        elif name == 'home':
            data_count_completion_date = await dbhome.count_home(username)
            data_completed = await dbcomp.completed_home()
        
        elif name == 'store':
            data_count_completion_date = await dbstore.count_store(username)
            data_completed = await dbcomp.completed_store()
        
        count_plane = await dbplan.select_count_plan()
        
        new_data_completed = []
        for i, d in enumerate(data_completed, 1):
            if len(list(d)) == 2:
                dc = list(d) + [False] + [i]
            else:
                dc = list(d) + [i]
            new_data_completed.append(dc)
        
        return templates.TemplateResponse(
            "completed.html",
            {
                "request": request,
                "data_count_all_priority": data_count_completion_date.count_priority,
                "data_count_all_user_name": data_count_completion_date.count_user_name,
                "data_count_all_completion_date": data_count_completion_date.count_completion_date,
                "data_count_all_checkbox_true": data_count_completion_date.count_checkbox_true,
                "data_count_all_checkbox_false": data_count_completion_date.count_checkbox_false,
                "data_count": count_plane,
                "data_completed": new_data_completed
            }
        )
        
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    
    
@router.post("/delete_completed")
async def delete_completed_post(request: Request, data_comp: DeletComplet, user: dict = Depends(get_current_user)):
    
    if user:
        
        if not data_comp.sprice:
            data_comp.sassigned = data_comp.sassigned.split(': ')[1]
            name_c = 'home'
        else:
            name_c = 'store'
        
        await dbcomp.delete_completed(data_comp.pcontent, data_comp.sassigned, data_comp.sprice)
        
        return JSONResponse(content={
            'message': 'ok plan',
            'data': f'/completed?name={name_c}'
        })
        
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    

@router.post("/delete_selected_completed")
async def delete_selected_completed_post(request: Request, data_del: DeleteSelectedCompleted, user: dict = Depends(get_current_user)):

    if user:
        print(data_del)
        return JSONResponse(content={
            'message': 'ok',
            'data': '/'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
