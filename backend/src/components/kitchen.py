from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from data.schemas import OrderDetails
from data.models import OrderedItems
from random import randint
from .dependencies import get_db

router = APIRouter()

@router.get("/orders/kitchen/")
async def view_kitchen_orders(db: Session = Depends(get_db)):
    try:
        items = db.query(OrderedItems).filter(OrderedItems.order_state == "cook").all()
        kitchen_list = [
            {
                "order_id": item.order_id,
                "time_created": item.time_created,
                "order_status": item.order_state,
                "table_num": item.table_number,
                "pickup_number": item.pickup_number,
                "pickup": item.pickup,
                "category": item.category,
                "amount_ordered": item.amount_ordered,
                "name": item.name,
                "price": item.price,
            }
            for item in items
        ]

        return {"kitchen_list": kitchen_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve kitchen orders")


@router.post("/orders/kitchen/")
async def add_kitchen_order(order: OrderDetails, db: Session = Depends(get_db)):
    try:
        with open("data_files/unpaid_orders.txt", "r") as file_object:
            orders_pending = [line.split()[0] for line in file_object.readlines()]

        # Generate a new pickup number if it's a pickup order
        new_pickup_number = randint(0, 100) if order.pickup else None

        # Check if the table number already has an order placed
        if order.table_num is not None and str(order.table_num) in orders_pending:
            return {"message": f"Table {order.table_num} already has an order placed"}

        # Add individual items to the database
        for item in order.ordered_list:
            new_item = OrderedItems(
                order_state="cook",
                table_number=order.table_num,
                pickup_number=new_pickup_number,
                pickup=order.pickup,
                category=item.category,
                amount_ordered=item.amount_ordered,
                name=item.item_name,
                price=item.price,
            )
            db.add(new_item)
            db.commit()
            db.refresh(new_item)

        # Add order details to the text file
        with open("data_files/unpaid_orders.txt", "a") as order_file:
            order_file.write(f"{order.table_num} {order.json()}\n")

        # Return appropriate message based on order type
        if order.pickup:
            return {"message": new_pickup_number}
        else:
            return {"message": f"Table {order.table_num} has placed an order in the queue"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to add kitchen order")


@router.post("/orders/kitchen/{order_id}")
async def complete_kitchen_order(order_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(OrderedItems).filter(OrderedItems.order_id == order_id, OrderedItems.order_state == "cook").one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Order ID does not exist or is not part of the kitchen staff queue")

    # Update the order state to "ready" (preparing for pickup by wait staff)
    setattr(item, "order_state", "ready")
    db.commit()
    
    return {"message": f"Order ID {order_id} has been removed from the kitchen order queue and added to the wait staff queue"}
