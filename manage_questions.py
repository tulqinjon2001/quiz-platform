# manage_questions.py
import json
from sqlalchemy import text
from app.database import SessionLocal, engine
from app import models

def replace_questions(path="questions.json"):
    # Jadval tuzilmalari mavjudligiga ishonch hosil qilamiz
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # FK lar bo'lsa ham xavfsiz tozalash
        db.execute(text("TRUNCATE TABLE results RESTART IDENTITY CASCADE;"))
        db.execute(text("TRUNCATE TABLE sessions RESTART IDENTITY CASCADE;"))
        db.execute(text("TRUNCATE TABLE questions RESTART IDENTITY CASCADE;"))
        db.commit()
    except Exception:
        # Agar TRUNCATE ishlamasa - fallback DELETE
        db.rollback()
        try:
            db.query(models.Result).delete()
            db.query(models.Session).delete()
            db.query(models.Question).delete()
            db.commit()
        except Exception:
            db.rollback()
            raise

    # Yangi savollarni JSON dan yuklaymiz
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    objs = [
        models.Question(
            text=item["text"],
            options=item["options"],
            correct_option=item["correct_option"],
        )
        for item in data
    ]
    db.bulk_save_objects(objs)
    db.commit()

    # Nazorat uchun sanog'ini chiqaramiz
    count = db.execute(text("SELECT COUNT(*) FROM questions")).scalar_one()
    print(f"✅ Yuklandi: {count} ta savol.")
    db.close()

if __name__ == "__main__":
    replace_questions("questions.json")
