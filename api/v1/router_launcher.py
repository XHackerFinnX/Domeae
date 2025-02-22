import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter(
    prefix="",
    tags=["Launcher"]
)

templates = Jinja2Templates(directory=r"./templates")

@router.get("/launcher/versions")
def get_download():
    file_path = r"./db/file_json/launcher.json"
    with open(file_path, "r") as file:
        data = json.load(file)
        
    return JSONResponse(content=data)