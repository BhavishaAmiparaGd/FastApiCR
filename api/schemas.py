from pydantic import BaseModel

class ItemBase(BaseModel):
    username: str
    email: str
    password: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
