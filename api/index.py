from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR / "q-fastapi.csv")

students = df.to_dict(orient="records")


@app.get("/")
def home():
    return {"status": "ok"}


@app.get("/api")
def get_students(
    class_: list[str] | None = Query(
        default=None,
        alias="class"
    )
):

    if not class_:
        return {
            "students": students
        }

    filtered = [
        row
        for row in students
        if row["class"] in class_
    ]

    return {
        "students": filtered
    }
