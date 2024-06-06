from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from data import UserDelete, UserAdd, Users
from .dependencies import get_db

router = APIRouter()

@router.post("/users")
async def add_user(user: UserAdd, db: Session = Depends(get_db)):
    valid_user_types = ["Manager", "VIP", "Staff"]

    if user.user_type not in valid_user_types:
        raise HTTPException(status_code=400, detail="Invalid user type")

    try:
        curr_user = db.query(Users).filter(Users.key == user.key_curr).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User attempting to add another user does not exist")

    if curr_user.user_type not in ["Manager", "Staff"]:
        raise HTTPException(status_code=403, detail="Permission denied: user type unable to add user")

    if curr_user.user_type == "Staff" and user.user_type == "Manager":
        raise HTTPException(status_code=403, detail="Permission denied: staff cannot add manager user type")

    try:
        db.query(Users).filter(Users.key == user.key_add).one()
        raise HTTPException(status_code=400, detail="User already exists")
    except NoResultFound:
        new_user = Users(key=user.key_add, user_type=user.user_type)
        db.add(new_user)
        db.commit()

    return {"message": "User has been successfully added"}


@router.delete("/users")
async def remove_user(user: UserDelete, db: Session = Depends(get_db)):
    try:
        curr_user = db.query(Users).filter(Users.key == user.key_curr).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User attempting to delete another user does not exist")

    if curr_user.user_type in ["VIP", "Staff"]:
        raise HTTPException(status_code=403, detail="Permission denied: user type unable to delete user")

    try:
        user_to_delete = db.query(Users).filter(Users.key == user.key_del).one()
        db.delete(user_to_delete)
        db.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User does not exist")

    return {"message": "User successfully deleted"}
