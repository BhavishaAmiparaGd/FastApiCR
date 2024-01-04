import logging
from urllib import request
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import HTMLResponse
from database.connection import SessionLocal
from fastapi.templating import Jinja2Templates
from . import crud, schemas
from database.connection import engine
from . import models
from .crud import  verify_password, verify_user_by_email
router = APIRouter()
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="frontend/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/register/", response_class=HTMLResponse)
async def register_user(
        request: Request,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user_data = schemas.ItemCreate(username=username, email=email, password=password)
    created_user = crud.create_user(db=db, Item=user_data)

    if created_user:
        return templates.TemplateResponse("login.html", {"request": request})
    else:

        return templates.TemplateResponse("registration_failed.html", {"request": request})


@router.post("/login/", response_class=HTMLResponse)
async def login_user(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user = crud.verify_user_by_email(db, email, password)

    if user:
        return templates.TemplateResponse("dashboard.html", {"request": request})
    else:
        return "invalid username and password"







@router.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@router.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

@router.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.update_item(db=db, item_id=item_id, item=item)

@router.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.delete_item(db=db, item_id=item_id)