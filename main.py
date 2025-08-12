from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path

DB = Path("tasks.json")
if not DB.exists():
    DB.write_text("[]")

class Task(BaseModel):
    id: int | None = None
    title: str
    done: bool = False

app = FastAPI(title="Tasks API")

def read_db():
    return json.loads(DB.read_text())

def write_db(data):
    DB.write_text(json.dumps(data, indent=2))

@app.get("/tasks")
def list_tasks():
    return read_db()

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    data = read_db()
    task.id = (max([t['id'] for t in data], default=0) + 1) if data else 1
    data.append(task.dict())
    write_db(data)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    data = read_db()
    new = [t for t in data if t['id'] != task_id]
    if len(new) == len(data):
        raise HTTPException(status_code=404, detail="Not found")
    write_db(new)
    return None
