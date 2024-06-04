from sqlalchemy import Boolean, Column, Float, Integer, String
from .database import Base
from datetime import datetime

# https://www.geeksforgeeks.org/fastapi-sqlite-databases/

# Database model
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    key = Column(String, unique=True, nullable=False)  # for logging in
    user_type = Column(String, nullable=False)  # User Types: Manager, Staff, VIP
    # email = Column(String, unique=True, nullable=True) # for VIP??
    # logged_in = Column(Boolean, nullable=False, default=False) MAYBE??

class Tables(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    table_number = Column(Integer, unique=True, nullable=False)
    occupied = Column(Boolean, default=False, nullable=False)

class MenuItems(Base):
    __tablename__ = "menuitems"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    vip_price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    image = Column(Integer, nullable=True)
    # string determining type of food ("dessert, main, etc")

class OrderedItems(Base):
    __tablename__ = "ordereditems"
    order_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    pickup_number = Column(Integer, nullable=True)
    time_created = Column(String, default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), nullable=False)
    order_state = Column(String, nullable=False)
    table_number = Column(Integer, nullable=True)
    amount_ordered = Column(Integer, nullable=False)
    pickup = Column(Boolean, default=False, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

class Categories(Base):
    __tablename__ = "categories"
    category_name = Column(String, primary_key=True, unique=True, nullable=False)

class Feedbacks(Base):
    __tablename__ = "feedbacks"
    feedback_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    customer_name = Column(String, nullable=False)
    feedback_rating = Column(Integer, nullable=False)
    feedback_comment = Column(String, nullable=False)
    feedback_time = Column(String, default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), nullable=False)
