from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from db.session import DataBasEenemies
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="",
    tags=["Enemies"]
)

db = DataBasEenemies()

class Person(BaseModel):
    name: str
    
templates = Jinja2Templates(directory=r"./templates")

@router.get("/people")
async def get_all_people(request: Request):
    return templates.TemplateResponse("enemies.html", {"request": request})

@router.post("/people/name")
async def get_all_people():
    name_list = await db.select_name()
    return JSONResponse(content=name_list)

@router.post("/people/add")
async def add_new_person(person: Person):
    await db.add_name(person.name)
    return {'ok': True}

@router.delete("/people/{person_id}")
async def delete_person_by_id(person_id: int):
    await db.delete_name(person_id)
    return {"message": f"Person with id {person_id} deleted."}
