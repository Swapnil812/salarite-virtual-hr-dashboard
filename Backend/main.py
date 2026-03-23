from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine, Base
from models import Task

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Backend is up and running 🚀"}

@app.get("/tasks")
def fetch_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


@app.post("/tasks")
def add_task(title: str, description: str, db: Session = Depends(get_db)):
    new_task = Task(
        title=title,
        description=description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    status: str,
    interview_mode: str,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        return {"error": "Task not found"}

    # Update fields
    task.status = status
    task.interview_mode = interview_mode

    db.commit()

    return task