from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from data import UserLogin, Users
from .dependencies import get_db

router = APIRouter()

@router.post("/login")
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(Users.key == user_login.key, Users.user_type == user_login.user_type).one()
        db.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")

    return {"user login successful": user_login.key}
