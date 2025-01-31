from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/blog/{id}")
def show(id: int):
    return {"data": id}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post("/blog")
def create_blog(request: Blog):
    return {"data": f"Blog is created as {request.title}"}
