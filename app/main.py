from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .quiz import router as quiz_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# <-- CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # agar prod domen bo'lsa shu yerga qo'shing: "https://your-frontend.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -->

app.include_router(quiz_router)
