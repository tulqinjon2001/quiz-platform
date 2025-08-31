from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .quiz import router as quiz_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS: test uchun keng ruxsat (Production’da aniq domenlarni yozasiz)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # vaqtincha *
    allow_credentials=False,    # * bilan True bo'lmasin
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quiz_router)
