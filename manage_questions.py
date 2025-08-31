# manage_questions.py
import json
from sqlalchemy import text, inspect
from app.database import SessionLocal, engine
from app import models

def replace_questions(path="questions.json"):
    # 1) jadvallar borligini ta'minlaymiz
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        insp = inspect(engine)
        has_results = insp.has_table("results")
        has_questions = insp.has_table("questions")

        # 2) mavjud bo'lsa TRUNCATE, aks holda DELETE yoki o'tkazib yuborish
        if has_results:
            try:
                db.execute(text("TRUNCATE TABLE results RESTART IDENTITY;"))
                db.commit()
            except Exception:
                db.rollback()
                db.query(models.Result).delete()
                db.commit()

        if has_questions:
            try:
                db.execute(text("TRUNCATE TABLE questions RESTART IDENTITY;"))
                db.commit()
            except Exception:
                db.rollback()
                db.query(models.Question).delete()
                db.commit()

        # 3) yangi savollarni yuklash
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
        print(f"✅ {len(objs)} ta savol bazaga yuklandi (replace).")

    finally:
        db.close()

if __name__ == "__main__":
    replace_questions("questions.json")
