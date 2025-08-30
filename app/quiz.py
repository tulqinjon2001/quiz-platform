from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, telegram
from .database import SessionLocal
import random

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/start-test/")
def start_test(payload: schemas.StartTestRequest, db: Session = Depends(get_db)):
    new_session = models.Session(name=payload.name, phone=payload.phone)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {"session_id": new_session.id}

@router.get("/get-questions/", response_model=list[schemas.QuestionOut])
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(models.Question).all()
    if len(questions) < 30:
        raise HTTPException(status_code=400, detail="Not enough questions in the database.")
    selected = random.sample(questions, 30)
    return selected

@router.post("/submit-answers/", response_model=schemas.ResultOut)
def submit_answers(payload: schemas.SubmitAnswersRequest, db: Session = Depends(get_db)):
    questions = db.query(models.Question).filter(models.Question.id.in_(payload.answers.keys())).all()
    score = 0
    for q in questions:
        if payload.answers.get(q.id) == q.correct_option:
            score += 1

    result = models.Result(
        session_id=payload.session_id,
        score=score,
        submitted_answers=payload.answers
    )
    db.add(result)
    db.commit()

    # Telegramga yuborish
    session = db.query(models.Session).filter(models.Session.id == payload.session_id).first()
    telegram.send_result(name=session.name, phone=session.phone, score=score)

    return {"score": score}
