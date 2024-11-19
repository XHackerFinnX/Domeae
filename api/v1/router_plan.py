from math import fabs
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from api.v1.router_auth import get_current_user
from pydantic import BaseModel

from db.session import DataBasePlan, DataBaseHome, DataBaseStory, DataBaseStudy, DataBaseCountIndex

from datetime import datetime


router = APIRouter(
    prefix="",
    tags=["Plan"]
)

dbplan = DataBasePlan()
dbhome = DataBaseHome()
dbstore = DataBaseStory()
dbstudy = DataBaseStudy()
db_count = DataBaseCountIndex()

class ContentUpdateRequest(BaseModel):
    title: str
    
class ModalPlan(BaseModel):
    case_id: str
    case_text: str
    text_task: str
    
class UpdatePlan(BaseModel):
    task_id: str
    case_id: str
    text_case: str
    
class DeletePlan(BaseModel):
    case_id: str
    menu_text: str
    
templates = Jinja2Templates(directory=r"./templates")

@router.get("/plan")
async def plan_get(request: Request, user: dict = Depends(get_current_user)):
    
    if user:
        
        if user == 35:
            username = 'Лёше'
        
        elif user == 807:
            username = 'Снеже'
        
        data_count_all = await db_count.select_count_all(username)
        data_plan = await dbplan.select_data_plan()
        count_plane = await dbplan.select_count_plan()
        
        new_data_plan = []
        
        for i in data_plan[0]:
            t = i[0], i[1], i[2].split('\n')
            new_data_plan.append(t)

        return templates.TemplateResponse(
            "plan.html",
            {
                "request": request,
                "data_plan": new_data_plan,
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

@router.post("/plan_v")
async def plan_post(request: Request, user: dict = Depends(get_current_user)):
    
    if user:
        return JSONResponse(content={
                'message': 'plan',
                'data': '/plan'
            })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    
    
@router.post("/plan_modal")
async def plan_modal_post(request: Request, data_plan: ModalPlan, user: dict = Depends(get_current_user)):
    
    if user:
        
        num_plan = await dbplan.case_id_plan(data_plan.case_id)
        date_c = datetime.now()
        
        await dbplan.insert_plan(
            user_id=user,
            case_id=data_plan.case_id,
            num_case_id=num_plan,
            case_text=data_plan.case_text,
            text_task=data_plan.text_task,
            checkbox=False,
            date_create=date_c
        )
        
        return JSONResponse(content={
            'message': 'ok plan',
            'data': '/plan'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    
    
@router.post("/update_checkbox_plan")
async def update_checkbox_plan_post(request: Request, dataupdate_plan: UpdatePlan, user: dict = Depends(get_current_user)):
    
    if user:
        
        name_task  = dataupdate_plan.task_id
        case_id = dataupdate_plan.case_id.split('-')
        text_case = dataupdate_plan.text_case
        
        if user == 35:
            username = 'Лёше'
        
        elif user == 807:
            username = 'Снеже'
            

        if name_task == 'urgent':
            num_urgent = await dbhome.case_id_home(case_id=name_task)
            date_c = datetime.now()
        
            await dbhome.insert_home_task(
                user_id=int(user),
                case_id=name_task,
                num_case_id=num_urgent,
                case_text='Срочное дело',
                text_task=text_case,
                user_name=username,
                completion_date='Нет',
                priority=False,
                reminder=0,
                checkbox=False,
                date_create=date_c
            )
            
        elif name_task == 'normal':
            num_normal = await dbhome.case_id_home(case_id=name_task)
            date_c = datetime.now()
        
            await dbhome.insert_home_task(
                user_id=int(user),
                case_id=name_task,
                num_case_id=num_normal,
                case_text='Обычное дело',
                text_task=text_case,
                user_name=username,
                completion_date='Нет',
                priority=False,
                reminder=0,
                checkbox=False,
                date_create=date_c
            )
            
        elif name_task == 'regular':
            num_regular = await dbhome.case_id_home(case_id=name_task)
            date_c = datetime.now()
        
            await dbhome.insert_home_task(
                user_id=int(user),
                case_id=name_task,
                num_case_id=num_regular,
                case_text='Регулярное дело',
                text_task=text_case,
                user_name=username,
                completion_date='Нет',
                priority=False,
                reminder=0,
                checkbox=False,
                date_create=date_c
            )
            
        elif name_task == 'today':
            num_today = await dbstore.case_id_store(case_id=name_task)
            date_c = datetime.now()

            await dbstore.insert_store_task(
                user_id=int(user),
                case_id=name_task,
                num_case_id=num_today,
                case_text='Сегодня',
                text_task=text_case,
                user_name=username,
                completion_date='Нет',
                priority=False,
                reminder=0,
                sum_pay=0,
                checkbox=False,
                date_create=date_c
            )
            
        elif name_task == 'week':
            num_week = await dbstore.case_id_store(case_id=name_task)
            date_c = datetime.now()

            await dbstore.insert_store_task(
                user_id=int(user),
                case_id=name_task,
                num_case_id=num_week,
                case_text='На неделе',
                text_task=text_case,
                user_name=username,
                completion_date='Нет',
                priority=False,
                reminder=0,
                sum_pay=0,
                checkbox=False,
                date_create=date_c
            )
            
        elif name_task == 'month':
            num_month = await dbstore.case_id_store(case_id=name_task)
            date_c = datetime.now()

            await dbstore.insert_store_task(
                user_id=int(user),
                case_id=name_task,
                num_case_id=num_month,
                case_text='В течении месяца',
                text_task=text_case,
                user_name=username,
                completion_date='Нет',
                priority=False,
                reminder=0,
                sum_pay=0,
                checkbox=False,
                date_create=date_c
            )
            
        elif name_task == 'homework':
            num_homework = await dbstudy.case_id_study(case_id=name_task)
            date_c = datetime.now()

            await dbstudy.insert_study_task(
                user_id=int(user),
                case_id=name_task,
                num_case_id=num_homework,
                case_text='Домашние задания',
                text_task=text_case,
                priority=False,
                reminder=0,
                checkbox=False,
                date_create=date_c
            )
            
        elif name_task == 'exam':
            num_exam = await dbstudy.case_id_study(case_id=name_task)
            date_c = datetime.now()

            await dbstudy.insert_study_task(
                user_id=int(user),
                case_id=name_task,
                num_case_id=num_exam,
                case_text='Экзамены',
                text_task=text_case,
                priority=False,
                reminder=0,
                checkbox=False,
                date_create=date_c
            )
            
        await dbplan.update_checkbox_true(case_id[0], int(case_id[2]))
        
        return JSONResponse(content={
            'message': 'ok plan',
            'data': '/plan'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})
    
    
@router.post("/update_menu_plan")
async def update_menu_plan_post(request: Request, datadelete_plan: DeletePlan, user: dict = Depends(get_current_user)):
    
    if user:
        
        if datadelete_plan.menu_text == 'Удалить план':
            case_id = datadelete_plan.case_id.split('-')
            await dbplan.delete_plan(case_id[0], int(case_id[1]))
        
        return JSONResponse(content={
            'message': 'ok plan',
            'data': '/plan'
        })
    else:
        return templates.TemplateResponse("auth.html", {"request": request})