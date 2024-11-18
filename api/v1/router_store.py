from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from api.v1.router_auth import get_current_user
from pydantic import BaseModel
from datetime import datetime

from db.session import DataBaseStory, DataBaseFilter, DataBasePlan
from db.models import main_completion_date_store

from api.v2.bot_notice import send_message_store_add, send_message_store_update

import asyncio


router = APIRouter(
    prefix="",
    tags=["Store"]
)

db = DataBaseStory()
db_filter = DataBaseFilter()
dbplan = DataBasePlan()

class ContentUpdateRequest(BaseModel):
    title: str
    
class DataStore(BaseModel):
    case_id: str
    case_text: str
    text_task: str
    user_name: str
    reminder: int
    
class UpdateCheckBox(BaseModel):
    case_id: str
    sum_pay: int
    
class UpdateMenu(BaseModel):
    case_id: str
    menu_text: str
    textp: str

templates = Jinja2Templates(directory=r"./templates")

@router.get("/store")
async def main_get(request: Request, user: dict = Depends(get_current_user)):
    
    if user:
        name_f = await db_filter.select_filter(user)
        
        if user == 35:
            username = 'Лёше'
        
        elif user == 807:
            username = 'Снеже'
        
        data_task = await db.select_data_store(username, name_f)
        data_count = await db.count_store(username)
        data_sum_pay = await db.sum_store()
        count_plane = await dbplan.select_count_plan()
        
        new_data_task_today = []
        new_data_task_week = []
        new_data_task_month = []

        for i in data_task.today:
            t = i[0], i[1], i[2].split('\n'), i[3], i[4], i[5]
            new_data_task_today.append(t)
            
        for i in data_task.week:
            t = i[0], i[1], i[2].split('\n'), i[3], i[4], i[5]
            new_data_task_week.append(t)
            
        for i in data_task.month:
            t = i[0], i[1], i[2].split('\n'), i[3], i[4], i[5]
            new_data_task_month.append(t)

        return templates.TemplateResponse(
            name = "store.html",
            context = {
                "request": request,
                "data_today": new_data_task_today,
                "data_week": new_data_task_week,
                "data_month": new_data_task_month,
                "data_count": data_count,
                "data_sum_pay": data_sum_pay,
                "data_filter": name_f,
                "data_count_plan": count_plane
            }
        )
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    
@router.post("/today")
async def post_today(request: Request, data_store: DataStore, user: dict = Depends(get_current_user)):
    
    if user:
        num_case = await db.case_id_store(case_id=data_store.case_id)
        
        date_c = datetime.now()
        
        await db.insert_store_task(
            user_id=int(user),
            case_id=data_store.case_id,
            num_case_id=num_case,
            case_text=data_store.case_text,
            text_task=data_store.text_task,
            user_name=data_store.user_name,
            completion_date='Нет',
            priority=False,
            reminder=data_store.reminder,
            sum_pay=0,
            checkbox=False,
            date_create=date_c
        )
        
        if user == 35:
            username = 'Лёше'
            chat_id = 1604126296
        
        elif user == 807:
            username = 'Снеже'
            chat_id = 1387002896

        await send_message_store_add(
            chat_id,
            data_store.case_text,
            data_store.text_task,
            data_store.user_name
        )
        
        return JSONResponse(content={
            'message': 'ok today',
            'data': '/store'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})

    
@router.post("/week")
async def post_week(request: Request, data_store: DataStore, user: dict = Depends(get_current_user)):
    
    if user:
        num_case = await db.case_id_store(case_id=data_store.case_id)
        
        date_c = datetime.now()
        
        await db.insert_store_task(
            user_id=int(user),
            case_id=data_store.case_id,
            num_case_id=num_case,
            case_text=data_store.case_text,
            text_task=data_store.text_task,
            user_name=data_store.user_name,
            completion_date='Нет',
            priority=False,
            reminder=data_store.reminder,
            sum_pay=0,
            checkbox=False,
            date_create=date_c
        )
        
        if user == 35:
            username = 'Лёше'
            chat_id = 1604126296
        
        elif user == 807:
            username = 'Снеже'
            chat_id = 1387002896

        await send_message_store_add(
            chat_id,
            data_store.case_text,
            data_store.text_task,
            data_store.user_name
        )
        
        return JSONResponse(content={
            'message': 'ok week',
            'data': '/store'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    

@router.post("/month")
async def post_month(request: Request, data_store: DataStore, user: dict = Depends(get_current_user)):
    
    if user:
        num_case = await db.case_id_store(case_id=data_store.case_id)
        
        date_c = datetime.now()
        
        await db.insert_store_task(
            user_id=int(user),
            case_id=data_store.case_id,
            num_case_id=num_case,
            case_text=data_store.case_text,
            text_task=data_store.text_task,
            user_name=data_store.user_name,
            completion_date='Нет',
            priority=False,
            reminder=data_store.reminder,
            sum_pay=0,
            checkbox=False,
            date_create=date_c
        )
        
        if user == 35:
            username = 'Лёше'
            chat_id = 1604126296
        
        elif user == 807:
            username = 'Снеже'
            chat_id = 1387002896

        await send_message_store_add(
            chat_id,
            data_store.case_text,
            data_store.text_task,
            data_store.user_name
        )
        
        return JSONResponse(content={
            'message': 'ok month',
            'data': '/store'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    
    
@router.post("/update_checkbox_store")
async def store_checkbox(request: Request, data_checkbox: UpdateCheckBox, user: dict = Depends(get_current_user)):
    
    if user:
        dcb = data_checkbox.case_id.split('-')
        
        await db.update_checkbox_store(dcb[0], int(dcb[2]), int(data_checkbox.sum_pay))
        
        return JSONResponse(content={
            'message': 'ok checkbox',
            'data': '/store'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    
    
@router.post("/update_menu_store")
async def store_menu(request: Request, data_menu: UpdateMenu, user: dict = Depends(get_current_user)):
    
    if user:
        dun = data_menu.case_id.split('-')
        text_m = data_menu.menu_text
        text_p = data_menu.textp

        if user == 35:
            username = 'Лёше'
            chat_id = 1604126296
        
        elif user == 807:
            username = 'Снеже'
            chat_id = 1387002896
        
        if len(dun) == 3:
            
            if dun[2] == '1':
                
                await db.update_user_name_store(dun[0], int(dun[1]), text_m)
                
                await send_message_store_update(chat_id, text_p, f'Назначено {text_m}')
                
            elif dun[2] == '4':
                
                await db.update_priority_store(dun[0], int(dun[1]), True)
                
            elif dun[2] == '5':
                
                await db.update_priority_store(dun[0], int(dun[1]), False)
                
            elif dun[2] == '6':
                
                await db.delete_task_store(dun[0], int(dun[1]))
            
        elif len(dun) == 4:
            
            if dun[2] == '2':
                
                await db.update_completion_date_store(dun[0], int(dun[1]), text_m)
                
                try:
                    _ = asyncio.run(await main_completion_date_store(
                        dun[0],
                        int(dun[1]),
                        db.select_completion_date_store,
                        db.update_checkbox_store,
                        db.update_completion_date_store
                    ))
                    
                except RuntimeError:
                    print("Срок завершения")
                    
                await send_message_store_update(chat_id, text_p, f'Срок завершения изменился')

            elif dun[2] == '3':
                
                if text_m == 'Сегодня':
                    
                    num_case = await db.case_id_store(case_id='today')
                    
                    await db.update_case_store('today', num_case, dun[0], int(dun[1]), 'Сегодня')
                    
                    await send_message_store_update(chat_id, text_p, f'Переместили в Сегодня')
                
                elif text_m == 'На неделе':
                    
                    num_case = await db.case_id_store(case_id='week')
                    
                    await db.update_case_store('week', num_case, dun[0], int(dun[1]), 'На неделе')
                    
                    await send_message_store_update(chat_id, text_p, f'Переместили в На неделе')
                
                elif text_m == 'В течении месяца':
                    
                    num_case = await db.case_id_store(case_id='month')
                    
                    await db.update_case_store('month', num_case, dun[0], int(dun[1]), 'В течении месяца')
                    
                    await send_message_store_update(chat_id, text_p, f'Переместили В течении месяца')
        
        return JSONResponse(content={
            'message': 'ok menu_update_store',
            'data': '/store'
        })
        
    else:
        return templates.TemplateResponse("auth.html", {"request": request})