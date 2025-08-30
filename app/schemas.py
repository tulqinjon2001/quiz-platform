from pydantic import BaseModel
from typing import List, Dict

class StartTestRequest(BaseModel):
    name: str
    phone: str

class QuestionOut(BaseModel):
    id: int
    text: str
    options: Dict[str, str]

class SubmitAnswersRequest(BaseModel):
    session_id: int
    answers: Dict[int, str]  # question_id: selected_option

class ResultOut(BaseModel):
    score: int
