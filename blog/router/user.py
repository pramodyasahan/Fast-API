from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from blog import schema, models
from blog.database import get_db
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post("/", response_model=schema.ShowUser)
def create_user(request: schema.User, db: Session = Depends(get_db)):
    return user.create(db=db, request=request)


@router.get('/{id}', response_model=schema.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db=db)
