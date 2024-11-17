from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from api.v1.router_auth import get_current_user
from pydantic import BaseModel

from db.session import DataBaseStudy, DataBasePlan

from datetime import datetime

router = APIRouter(
    prefix="",
    tags=["Study"]
)

db = DataBaseStudy()
dbplan = DataBasePlan()

class ContentUpdateRequest(BaseModel):
    title: str
    
class DataStudy(BaseModel):
    case_id: str
    case_text: str
    text_task: str
    reminder: int
    
class UpdateCheckBox(BaseModel):
    case_id: str
    
class UpdateMenu(BaseModel):
    case_id: str
    menu_text: str

templates = Jinja2Templates(directory=r"./templates")

@router.get("/study")
async def main_get(request: Request, user: dict = Depends(get_current_user)):
    
    if user:
        data_task = await db.select_data_study(user)
        data_count = await db.count_study(user)
        count_plane = await dbplan.select_count_plan()

        new_data_task_homework = []
        new_data_task_exam = []
        
        for i in data_task.homework:
            t = i[0], i[1], i[2].split('\n'), i[3]
            new_data_task_homework.append(t)
            
        for i in data_task.exam:
            t = i[0], i[1], i[2].split('\n'), i[3]
            new_data_task_exam.append(t)
        
        return templates.TemplateResponse(
            name = "study.html",
            context = {
                "request": request,
                "data_homework": new_data_task_homework,
                "data_exam": new_data_task_exam,
                "data_count": data_count,
                "data_count_plan": count_plane
            }
        )
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    

@router.post("/homework")
async def homework_post(request: Request, data_study: DataStudy, user: dict = Depends(get_current_user)):
    
    if user:
        num_case = await db.case_id_study(case_id=data_study.case_id)
        
        date_c = datetime.now()
        
        await db.insert_study_task(
            user_id=int(user),
            case_id=data_study.case_id,
            num_case_id=num_case,
            case_text=data_study.case_text,
            text_task=data_study.text_task,
            priority=False,
            reminder=data_study.reminder,
            checkbox=False,
            date_create=date_c
        )
        
        return JSONResponse(content={
            'message': 'ok homework',
            'data': '/study'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    

@router.post("/exam")
async def homework_post(request: Request, data_study: DataStudy, user: dict = Depends(get_current_user)):
    
    if user:
        num_case = await db.case_id_study(case_id=data_study.case_id)
        
        date_c = datetime.now()
        
        await db.insert_study_task(
            user_id=int(user),
            case_id=data_study.case_id,
            num_case_id=num_case,
            case_text=data_study.case_text,
            text_task=data_study.text_task,
            priority=False,
            reminder=data_study.reminder,
            checkbox=False,
            date_create=date_c
        )
        
        return JSONResponse(content={
            'message': 'ok exam',
            'data': '/study'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    
    
@router.post("/update_checkbox_study")
async def study_checkbox(request: Request, data_checkbox: UpdateCheckBox, user: dict = Depends(get_current_user)):
    
    if user:
        dcb = data_checkbox.case_id.split('-')
        
        await db.update_checkbox_study(dcb[0], int(dcb[2]))
        
        return JSONResponse(content={
            'message': 'ok study',
            'data': '/study'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    

@router.post("/update_menu_study")
async def study_menu(request: Request, data_menu: UpdateMenu, user: dict = Depends(get_current_user)):
    
    if user:
        dun = data_menu.case_id.split('-')
        
        if dun[2] == '4':
            
            await db.update_priority_study(dun[0], int(dun[1]), True)
            
        elif dun[2] == '5':
            
            await db.update_priority_study(dun[0], int(dun[1]), False)
            
        elif dun[2] == '6':
            
            await db.delete_task_study(dun[0], int(dun[1]))
        
        return JSONResponse(content={
            'message': 'ok menu_update_study',
            'data': '/study'
        })
        
    else:
        return templates.TemplateResponse("auth.html", {"request": request})