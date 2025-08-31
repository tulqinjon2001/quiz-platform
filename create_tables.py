# create_tables.py  <-- app/ bilan BIR PAPKADA turadi
from app.database import engine, Base
from app import models  # modellarning ro'yxatdan o'tishi uchun MUHIM import

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
