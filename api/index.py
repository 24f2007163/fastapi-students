# api/index.py

from fastapi import FastAPI, Query, Response
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin"],
)

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR / "q-fastapi.csv")

students = df.to_dict(orient="records")


@app.get("/")
def home():
    return {"status": "ok"}


@app.options("/{path:path}")
def options_handler(path: str):
    return Response()


@app.get("/api")
def get_students(
    class_: list[str] | None = Query(
        default=None,
        alias="class"
    )
):

    if class_ is None or len(class_) == 0:
        return students

    filtered_students = [
        student
        for student in students
        if student["class"] in class_
    ]

    return filtered_students
