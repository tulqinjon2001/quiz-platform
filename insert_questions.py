import json
from sqlalchemy.orm import Session
from app.models import Question
from app.database import SessionLocal

# Savollar JSON fayldan yuklanadi
def load_questions_from_json(path: str):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def insert_questions():
    db: Session = SessionLocal()
    try:
        data = load_questions_from_json("questions.json")
        for item in data:
            q = Question(
                text=item["text"],
                options=item["options"],
                correct_option=item["correct_option"]
            )
            db.add(q)
        db.commit()
        print("✅ Savollar bazaga yuklandi.")
    finally:
        db.close()

if __name__ == "__main__":
    insert_questions()
