from fastapi import BackgroundTasks, FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from autoinstall import models, schemas
from autoinstall.database import engine, iter_db, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
from autoinstall import curd
from concurrent.futures import ThreadPoolExecutor
import time
from loguru import logger
from autoinstall.utils import iter_scanned_file

tp = ThreadPoolExecutor(10)

def scan_folder():
    logger.info("scan_folder")
    try:
        while True:
            db = SessionLocal()
            for file in iter_scanned_file(db):
                curd.check_file(db, file)
            time.sleep(10)
    except:
        logger.exception("scan_folder")
    finally:
        db.close()


@app.on_event('startup')
async def app_startup():
    tp.submit(scan_folder)


@app.get("/send-genereate_nsis/")
async def get_nsis(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(genereate_nsis, email, message="some notification")
    return {"message": "Notification sent in the background"}


@app.post("/api/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/install_file/", response_model=List[schemas.InstallFile])
async def list_install_file(skip: int = 0, limit: int = 100, db: Session = Depends(iter_db)) -> List[
    schemas.InstallFile]:
    res = curd.get_install_file(db=db)
    return res


@app.post("/api/scan_folder", response_model=schemas.ScanFolder)
async def create_scan_folder(scan_folder: schemas.ScanFolderAdd, db: Session = Depends(iter_db)) -> schemas.ScanFolder:
    print(scan_folder)
    obj = curd.create_scan_folder(db, scan_folder.path)
    return obj
