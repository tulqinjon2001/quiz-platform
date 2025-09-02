from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .quiz import router as quiz_router

app = FastAPI()

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # test uchun barcha domenlarga ruxsat
    allow_credentials=False,     # "*" bilan True bo'lmaydi
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB jadval yaratish - ilova ishga tushganda
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

# Routerlarni ulash
app.include_router(quiz_router)
