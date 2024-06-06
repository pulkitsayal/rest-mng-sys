from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from data import Feedback, Feedbacks
from .dependencies import get_db

router = APIRouter()

@router.get("/feedbacks/")
async def view_feedback(db: Session = Depends(get_db)):
    feedbacks = db.query(Feedbacks).all()

    feedback_list = [
        {
            "id": feedback.feedback_id,
            "name": feedback.customer_name,
            "rating": feedback.feedback_rating,
            "comment": feedback.feedback_comment,
            "time": feedback.feedback_time,
        }
        for feedback in feedbacks
    ]
    
    return {"feedbacks": feedback_list}


@router.post("/feedbacks/{feedback_name}")
async def add_feedback(feedback: Feedback, db: Session = Depends(get_db)):
    new_feedback = Feedbacks(
        customer_name=feedback.name,
        feedback_rating=feedback.rating,
        feedback_comment=feedback.comment,
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return {"message": f"Feedback from {feedback.name} has been successfully added"}


@router.delete("/feedbacks/{feedback_id}")
async def remove_feedback(feedback_id: int, db: Session = Depends(get_db)):
    try:
        db.query(Feedbacks).filter(Feedbacks.feedback_id == feedback_id).delete()
        db.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Feedback not found")

    return {"message": f"Feedback with ID {feedback_id} has been removed"}
