from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter(
    prefix="",
    tags=["Launcher"]
)

@router.get("/file/download/1201-forge-zip")
def download_file():
    file_path = Path('./db/file_zip/forge_1_20_1/forge_1_20_1.zip').resolve()
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename='forge1.20.1.zip', media_type='application/octet-stream')

@router.get("/file/download/1201-mods-1-zip")
def download_file():
    file_path = Path('./db/file_zip/mods_1_20_1/1_mods.zip').resolve()
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename='1_mods.zip', media_type='application/octet-stream')

@router.get("/file/download/1201-mods-2-zip")
def download_file():
    file_path = Path('./db/file_zip/mods_1_20_1/2_mods.zip').resolve()
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename='2_mods.zip', media_type='application/octet-stream')

@router.get("/file/download/1201-mods-3-zip")
def download_file():
    file_path = Path('./db/file_zip/mods_1_20_1/3_mods.zip').resolve()
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename='3_mods.zip', media_type='application/octet-stream')