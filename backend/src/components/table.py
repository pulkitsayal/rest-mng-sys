from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from data.models import Tables
from datetime import datetime, timedelta
from .dependencies import get_db

router = APIRouter()

@router.get("/tables/available")
async def view_available_tables(db: Session = Depends(get_db)):
    try:
        available_tables = db.query(Tables).filter(Tables.occupied == False).all()
        table_list = [table.table_number for table in available_tables]
        return {"tables": table_list}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")


@router.post("/tables/{table_num}")
async def select_table(table_num: int, db: Session = Depends(get_db)):
    if table_num == -1:
        return {"detail": "pickup order"}

    if table_num <= 0:
        raise HTTPException(status_code=404, detail="Invalid table number")

    curr_time = datetime.now()
    booking_file = "data_files/table_booking.txt"
    date_str = curr_time.strftime("%d/%m/%Y")

    try:
        with open(booking_file, "r") as file_object:
            for line in file_object:
                if f"{table_num} {date_str}" in line:
                    book_time = datetime.strptime(line.split()[2], "%H:%M")
                    curr_time_hour = datetime.strptime(curr_time.strftime("%H:%M"), "%H:%M")

                    if (book_time - timedelta(hours=1)) < curr_time_hour < (book_time + timedelta(hours=1)):
                        raise HTTPException(status_code=404, detail=f"Table {table_num} is already booked for that time")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Booking file not found")

    try:
        table_status = db.query(Tables).filter(Tables.table_number == table_num, Tables.occupied == False).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Table is already occupied")

    table_status.occupied = True
    db.commit()
    return {"message": f"Table {table_num} successfully booked", "occupied": table_status.occupied}


@router.post("/tables/booking")
async def book_table(table_num: int, book_time: str):
    book_time_obj = datetime.strptime(book_time, "%d/%m/%Y %H:%M")

    # Read existing bookings
    with open("data_files/table_booking.txt", "r") as file_object:
        for line in file_object:
            existing_table_num, existing_date, existing_time = line.strip().split(" ")
            existing_book_time = datetime.strptime(f"{existing_date} {existing_time}", "%d/%m/%Y %H:%M")

            # Check if the requested table and date match an existing booking
            if int(existing_table_num) == table_num and existing_book_time.date() == book_time_obj.date():
                # Calculate time difference
                prev_book_time = existing_book_time.time()
                new_book_time = book_time_obj.time()

                # Ensure the booking time is not within an hour before or after the existing booking
                if (datetime.combine(existing_book_time.date(), prev_book_time) - timedelta(hours=1) <=
                    datetime.combine(book_time_obj.date(), new_book_time) <=
                    datetime.combine(existing_book_time.date(), prev_book_time) + timedelta(hours=1)):
                    raise HTTPException(
                        status_code=404, 
                        detail=f"Table {table_num} is already booked for the time around {existing_time} on {existing_date}"
                    )

    # Write the new booking
    with open("data_files/table_booking.txt", "a") as file_object:
        file_object.write(f"{table_num} {book_time_obj.strftime('%d/%m/%Y %H:%M')}\n")

    return {"message": f"Table {table_num} has been successfully booked for {book_time}"}


@router.get("/tables/booking")
async def table_bookings():
    with open("data_files/table_booking.txt", "r") as file_object:
        bookings = [line.strip().split() for line in file_object]
    return bookings
