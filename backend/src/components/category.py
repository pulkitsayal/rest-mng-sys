from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from data.models import Categories
from data.schemas import Category
from .dependencies import get_db

router = APIRouter()

@router.get("/categories/")
async def view_categories(db: Session = Depends(get_db)):
    categories = db.query(Categories).all()

    category_list = [{"category": cat.category_name} for cat in categories]
    return {"category_list": category_list}

@router.post("/categories/{category_name}")
async def add_category(category: Category, db: Session = Depends(get_db)):
    try:
        existing_category = db.query(Categories).filter(Categories.category_name == category.categoryName).one()
        raise HTTPException(status_code=400, detail="Category already exists")
    except NoResultFound:
        new_category = Categories(category_name=category.categoryName)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return {"message": "Category has been successfully added", "categoryName": category.categoryName}

@router.delete("/categories/{category_name}")
async def remove_category(category_name: str, db: Session = Depends(get_db)):
    try:
        db.query(Categories).filter(Categories.category_name == category_name).delete()
        db.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": f"Category '{category_name}' has been removed"}

@router.put("/categories/{category_name}/")
async def update_category(category_name: str, updated_category: Category, db: Session = Depends(get_db)):
    try:
        category = db.query(Categories).filter(Categories.category_name == category_name).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

    setattr(category, "category_name", updated_category.categoryName)

    db.commit()
    return {"message": f"Category updated to '{updated_category.categoryName}'"}
