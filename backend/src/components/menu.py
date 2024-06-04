import os
import base64
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from json import loads
from data.schemas import Menu, MenuUpdate
from data.models import MenuItems
from .dependencies import get_db
from pathlib import Path

router = APIRouter()

def menuFunction(db):
    menu_items = db.query(MenuItems).all()
    menu_list = []
    image_dir_base = "./Food_Images/"

    for item in menu_items:
        image_path = os.path.join(image_dir_base, f"{item.image}.jpeg")
        encoded_image_string = None

        if os.path.exists(image_path):
            try:
                with open(image_path, "rb") as image_file:
                    encoded_image_string = base64.b64encode(image_file.read()).decode('utf-8')
            except Exception as e:
                print(f"Error reading image {image_path}: {e}")

        menu_list.append(
            {
                "name": item.name,
                "category": item.category,
                "price": item.price,
                "vip_price": item.vip_price,
                "description": item.description,
                "image": encoded_image_string,
            }
        )

    return menu_list

@router.get("/menu/")
async def view_menu(db: Session = Depends(get_db)):
    menu_list = menuFunction(db)
    return {"menu_list": menu_list}

@router.get("/orders/detail/{table_num}")
async def order_details(table_num: int, db: Session = Depends(get_db)):
    if table_num == -1:
        return {"detail": "pickup order"}

    if table_num <= 0:
        raise HTTPException(status_code=404, detail="Invalid table number")

    order_det = None

    try:
        with open("data_files/unpaid_orders.txt", "r") as order_list:
            for line in order_list:
                if str(table_num) == line.split()[0]:
                    order_det = loads(line.split(" ", 1)[1])
                    break
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Order file not found")

    if order_det is None:
        raise HTTPException(status_code=404, detail="Order does not exist or has not been placed by customer")

    total_cost = 0
    total_cost_vip = 0
    items_list = []
    image_dir_base = "./Food_Images/"

    for ordered_item in order_det["ordered_list"]:
        try:
            item = db.query(MenuItems).filter(MenuItems.name == ordered_item["item_name"]).one()
            db.commit()

            image_path = os.path.join(image_dir_base, f"{item.image}.jpeg")
            encoded_image_string = None

            if os.path.exists(image_path):
                try:
                    with open(image_path, "rb") as image_file:
                        encoded_image_string = base64.b64encode(image_file.read()).decode('utf-8')
                except Exception as e:
                    print(f"Error reading image {image_path}: {e}")

            items_list.append(
                {
                    "name": item.name,
                    "category": item.category,
                    "price": item.price,
                    "vip_price": item.vip_price,
                    "image": encoded_image_string,
                }
            )

            total_cost += item.price * ordered_item["amount_ordered"]
            total_cost_vip += item.vip_price * ordered_item["amount_ordered"]
        except NoResultFound:
            raise HTTPException(status_code=404, detail=f"Menu item {ordered_item['item_name']} not found")

    return {
        "table number": table_num,
        "total cost": total_cost,
        "vip total cost": total_cost_vip,
        "item details": items_list,
    }


@router.post("/items/{item_name}")
async def add_item(item_id: Menu, db: Session = Depends(get_db)):
    try:
        item = db.query(MenuItems).filter(MenuItems.name == item_id.itemName).one()
        raise HTTPException(status_code=400, detail="Menu item already exists")
    except NoResultFound:
        # Find a unique file path for the image
        f_num = 0
        while True:
            file_path = f"Food_Images/{f_num}.jpeg"
            if not Path(file_path).is_file():
                break
            f_num += 1

        # Write the image to the file
        with open(file_path, "wb") as image_file:
            image_file.write(base64.b64decode(item_id.image64.encode()))

        # Create and add the new menu item
        new_item = MenuItems(
            name=item_id.itemName,
            category=item_id.itemCategory,
            price=item_id.itemPrice,
            vip_price=item_id.vipPrice,
            description=item_id.itemDescription,
            image=file_path
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return {"message": "Item has been successfully added", "itemName": item_id.itemName}


@router.delete("/items/{item_name}")
async def remove_item(item_name: str, db: Session = Depends(get_db)):
    try:
        # Retrieve the item from the database
        item = db.query(MenuItems).filter(MenuItems.name == item_name).one()
        image_path = f"Food_Images/{item.image}.jpeg"

        # Check if the item's image exists and delete it
        if item.image and os.path.exists(image_path):
            os.remove(image_path)

        # Delete the item from the database
        db.delete(item)
        db.commit()

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": f"Item '{item_name}' has been removed from the menu"}


@router.put("/items/{item_name}/")
async def update_item(item_name: str, item_id: MenuUpdate, db: Session = Depends(get_db)):
    try:
        item = db.query(MenuItems).filter(MenuItems.name == item_name).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update item properties
    if item_id.imageChanged:
        # Delete the old image file if it exists
        if item.image is not None:
            image_path = f"Food_Images/{item.image}.jpeg"
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # Save the new image file
        image_path = save_image(item_id.image64)

        # Update the item's image attribute
        setattr(item, "image", image_path)

    # Update other item properties
    setattr(item, "name", item_id.itemName)
    setattr(item, "category", item_id.itemCategory)
    setattr(item, "price", item_id.itemPrice)
    setattr(item, "vip_price", item_id.vipPrice)
    setattr(item, "description", item_id.itemDescription)

    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Item name already exists")

    return {"message": f"Item updated to '{item_id.itemName}'"}

def save_image(image64: str):
    image_data = base64.b64decode(image64.encode())
    image_dir = "Food_Images"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # Find a unique file path for the image
    f_num = 0
    while True:
        file_path = os.path.join(image_dir, f"{f_num}.jpeg")
        if not os.path.exists(file_path):
            break
        f_num += 1

    # Write the image to the file
    with open(file_path, "wb") as image_file:
        image_file.write(image_data)

    return f_num
