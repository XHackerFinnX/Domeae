from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from api.v1.router_auth import get_current_user
from pydantic import BaseModel
from datetime import datetime

from db.session import DataBaseHome, DataBaseFilter, DataBasePlan
from db.models import main_completion_date

from api.v2.bot_notice import send_message_home_add, send_message_home_update

import asyncio

router = APIRouter(
    prefix="",
    tags=["Home"]
)

db = DataBaseHome()
db_filter = DataBaseFilter()
dbplan = DataBasePlan()

class ContentUpdateRequest(BaseModel):
    title: str
    
class DataHome(BaseModel):
    case_id: str
    case_text: str
    text_task: str
    user_name: str
    reminder: int
    
class UpdateCheckBox(BaseModel):
    case_id: str
    
class UpdateMenu(BaseModel):
    case_id: str
    menu_text: str
    textp: str
    

templates = Jinja2Templates(directory=r"./templates")

@router.get("/home")
async def main_get(request: Request, user: dict = Depends(get_current_user)):
    
    if user:
        name_f = await db_filter.select_filter(user)
        
        if user == 35:
            username = 'Лёше'
        
        elif user == 807:
            username = 'Снеже'
        
        data_task = await db.select_data_home(username, name_f)
        data_count = await db.count_home(username)
        count_plane = await dbplan.select_count_plan()
        
        new_data_task_urgent = []
        new_data_task_normal = []
        new_data_task_regular = []

        for i in data_task.urgent:
            t = i[0], i[1], i[2].split('\n'), i[3], i[4], i[5]
            new_data_task_urgent.append(t)
            
        for i in data_task.normal:
            t = i[0], i[1], i[2].split('\n'), i[3], i[4], i[5]
            new_data_task_normal.append(t)
            
        for i in data_task.regular:
            t = i[0], i[1], i[2].split('\n'), i[3], i[4], i[5]
            new_data_task_regular.append(t)
        
        return templates.TemplateResponse(
            name = "home.html",
            context = {
                "request": request,
                "data_urgent": new_data_task_urgent,
                "data_normal": new_data_task_normal,
                "data_regular": new_data_task_regular,
                "data_count": data_count,
                "data_filter": name_f,
                "data_count_plan": count_plane
            }
        )
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    
    
@router.post("/urgent")
async def home_urgent(request: Request, data_home: DataHome, user: dict = Depends(get_current_user)):
    
    if user:
        num_case = await db.case_id_home(case_id=data_home.case_id)
        
        date_c = datetime.now()
        
        await db.insert_home_task(
            user_id=int(user),
            case_id=data_home.case_id,
            num_case_id=num_case,
            case_text=data_home.case_text,
            text_task=data_home.text_task,
            user_name=data_home.user_name,
            completion_date='Нет',
            priority=False,
            reminder=data_home.reminder,
            checkbox=False,
            date_create=date_c
        )
        
        if user == 35:
            username = 'Лёше'
            chat_id = 1604126296
        
        elif user == 807:
            username = 'Снеже'
            chat_id = 1387002896

        await send_message_home_add(
            chat_id,
            data_home.case_text,
            data_home.text_task,
            data_home.user_name
        )
        
        return JSONResponse(content={
            'message': 'ok urgent',
            'data': '/home'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})

    
@router.post("/normal")
async def home_normal(request: Request, data_home: DataHome, user: dict = Depends(get_current_user)):
    
    if user:
        num_case = await db.case_id_home(case_id=data_home.case_id)
        
        date_c = datetime.now()
        
        await db.insert_home_task(
            user_id=int(user),
            case_id=data_home.case_id,
            num_case_id=num_case,
            case_text=data_home.case_text,
            text_task=data_home.text_task,
            user_name=data_home.user_name,
            completion_date='Нет',
            priority=False,
            reminder=data_home.reminder,
            checkbox=False,
            date_create=date_c
        )
        
        if user == 35:
            username = 'Лёше'
            chat_id = 1604126296
        
        elif user == 807:
            username = 'Снеже'
            chat_id = 1387002896

        await send_message_home_add(
            chat_id,
            data_home.case_text,
            data_home.text_task,
            data_home.user_name
        )
        
        return JSONResponse(content={
            'message': 'ok normal',
            'data': '/home'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    
    
@router.post("/regular")
async def home_regular(request: Request, data_home: DataHome, user: dict = Depends(get_current_user)):
    
    if user:
        num_case = await db.case_id_home(case_id=data_home.case_id)
        
        date_c = datetime.now()
        
        await db.insert_home_task(
            user_id=int(user),
            case_id=data_home.case_id,
            num_case_id=num_case,
            case_text=data_home.case_text,
            text_task=data_home.text_task,
            user_name=data_home.user_name,
            completion_date='Нет',
            priority=False,
            reminder=data_home.reminder,
            checkbox=False,
            date_create=date_c
        )
        
        if user == 35:
            username = 'Лёше'
            chat_id = 1604126296
        
        elif user == 807:
            username = 'Снеже'
            chat_id = 1387002896

        await send_message_home_add(
            chat_id,
            data_home.case_text,
            data_home.text_task,
            data_home.user_name
        )
        
        return JSONResponse(content={
            'message': 'ok regular',
            'data': '/home'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    
@router.post("/update_checkbox")
async def home_checkbox(request: Request, data_checkbox: UpdateCheckBox, user: dict = Depends(get_current_user)):
    
    if user:
        dcb = data_checkbox.case_id.split('-')
        
        await db.update_checkbox_home(dcb[0], int(dcb[2]))
        
        return JSONResponse(content={
            'message': 'ok checkbox',
            'data': '/home'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    
    
@router.post("/update_menu")
async def home_menu(request: Request, data_username: UpdateMenu, user: dict = Depends(get_current_user)):
    
    if user:
        dun = data_username.case_id.split('-')
        text_m = data_username.menu_text
        text_p = data_username.textp

        if user == 35:
            username = 'Лёше'
            chat_id = 1604126296
        
        elif user == 807:
            username = 'Снеже'
            chat_id = 1387002896
            
        
        if len(dun) == 3:
            
            if dun[2] == '1':
                
                await db.update_user_name(dun[0], int(dun[1]), text_m)
                
                await send_message_home_update(chat_id, text_p, f'Назначено {text_m}')
                
            elif dun[2] == '4':
                
                await db.update_priority(dun[0], int(dun[1]), True)
                
            elif dun[2] == '5':
                
                await db.update_priority(dun[0], int(dun[1]), False)
                
            elif dun[2] == '6':
                
                await db.delete_task(dun[0], int(dun[1]))
            
        elif len(dun) == 4:
            
            if dun[2] == '2':
                
                await db.update_completion_date(dun[0], int(dun[1]), text_m)
                
                try:
                    _ = asyncio.run(await main_completion_date(
                        dun[0],
                        int(dun[1]),
                        db.select_completion_date,
                        db.update_checkbox_home,
                        db.update_completion_date
                    ))
                    
                except RuntimeError:
                    print("Срок завершения")
                
                await send_message_home_update(chat_id, text_p, f'Срок завершения {db.update_completion_date}')

            elif dun[2] == '3':
                
                if text_m == 'Срочное дело':
                    
                    num_case = await db.case_id_home(case_id='urgent')
                    
                    await db.update_case('urgent', num_case, dun[0], int(dun[1]), 'Срочное дело')
                    
                    await send_message_home_update(chat_id, text_p, f'Переместили в Срочное дело')
                
                elif text_m == 'Обычное дело':
                    
                    num_case = await db.case_id_home(case_id='normal')
                    
                    await db.update_case('normal', num_case, dun[0], int(dun[1]), 'Обычное дело')
                    
                    await send_message_home_update(chat_id, text_p, f'Переместили в Обычное дело')
                
                elif text_m == 'Регулярное дело':
                    
                    num_case = await db.case_id_home(case_id='regular')
                    
                    await db.update_case('regular', num_case, dun[0], int(dun[1]), 'Регулярное дело')
                    
                    await send_message_home_update(chat_id, text_p, f'Переместили в Регулярное дело')
        
        return JSONResponse(content={
            'message': 'ok menu_update',
            'data': '/home'
        })
        
    else:
        return templates.TemplateResponse("auth.html", {"request": request})