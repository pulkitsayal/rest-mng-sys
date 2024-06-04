from pydantic import BaseModel
from typing import List

# https://www.geeksforgeeks.org/fastapi-sqlite-databases/

# Pydantic model for data
class UserLogin(BaseModel):
    user_type: str
    key: str
    # logged_in: bool

class UserDelete(BaseModel):
    key_curr: str
    key_del: str

class UserAdd(BaseModel):
    key_curr: str
    key_add: str
    user_type: str

class OrderedItem(BaseModel):
    item_name: str
    amount_ordered: int
    category: str
    price: float

class OrderDetails(BaseModel):
    table_num: int
    pickup: bool
    ordered_list: List[OrderedItem]
    # time_created: 'enter a time stamp',
    pickup: bool

class Menu(BaseModel):
    itemName: str
    itemCategory: str
    itemPrice: float
    vipPrice: float
    itemDescription: str
    image64: str

class MenuUpdate(BaseModel):
    itemName: str
    itemCategory: str
    itemPrice: float
    vipPrice: float
    itemDescription: str
    image64: str
    imageChanged: bool

class Category(BaseModel):
    categoryName: str

class Feedback(BaseModel):
    name: str
    rating: int
    comment: str

class Stats(BaseModel):
    start_date: str
    end_date: str
