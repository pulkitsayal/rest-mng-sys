from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from data import OrderedItems
from .dependencies import get_db

router = APIRouter()

@router.get("/orders/waiter/")
async def view_waiter_orders(db: Session = Depends(get_db)):
    try:
        items = db.query(OrderedItems).filter(OrderedItems.order_state == "ready").all()
        waiter_list = [
            {
                "order_id": item.order_id,
                "time_created": item.time_created,
                "order_status": item.order_state,
                "table_num": item.table_number,
                "pickup_num": item.pickup_number,
                "pickup": item.pickup,
                "category": item.category,
                "amount_ordered": item.amount_ordered,
                "name": item.name,
                "price": item.price,
            }
            for item in items
        ]

        return {"waiter_list": waiter_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve waiter orders")

@router.post("/orders/waiter/{order_id}")
async def complete_waiter_order(order_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(OrderedItems).filter(OrderedItems.order_id == order_id, OrderedItems.order_state == "ready").one()
    except NoResultFound:
        raise HTTPException(status_code=400, detail="Order ID does not exist or is not part of the wait staff queue")

    setattr(item, "order_state", "completed")
    db.commit()
    return {"message": f"Order ID {order_id} has been removed from wait staff queue"}
