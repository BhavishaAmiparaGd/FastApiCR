from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def verify_user_by_email(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None
    return user


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(models.User).filter(models.User.id == item_id).first()

def create_user(db: Session, Item: schemas.ItemCreate):
    hashed_password = pwd_context.hash(Item.password)
    db_user = models.User(username=Item.username, email=Item.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def create_item(db: Session, item: schemas.ItemCreate):
#     db_item = models.User(**item.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

def create_item(db: Session, item: schemas.ItemCreate):
    hashed_password = pwd_context.hash(item.password)
    item_dict = item.dict()
    item_dict["password"] = hashed_password
    db_item = models.User(**item_dict)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = db.query(models.User).filter(models.User.id == item_id).first()

    if db_item:

        db_item.username = item.username
        db_item.email = item.email


        if item.password:
            hashed_password = pwd_context.hash(item.password)
            db_item.password = hashed_password

        db.commit()
        db.refresh(db_item)
    return db_item



def delete_item(db: Session, item_id: int):
    db_item = db.query(models.User).filter(models.User.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return db_item