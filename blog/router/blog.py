from fastapi import APIRouter, Depends, HTTPException
from typing import List

from ..oauth import get_current_user
from ..repository import blog
from blog import schema, models
from sqlalchemy.orm import Session

from blog.database import get_db

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)


@router.get('/', response_model=List[schema.ShowBlog])
def get_all(db: Session = Depends(get_db), get_current_user: schema.User = Depends(get_current_user)):
    return blog.get_all(db)


@router.post('/', status_code=201)
def create(request: schema.Blog, db: Session = Depends(get_db)):
    return blog.create(db, request)


@router.delete('/{id}', status_code=204)
def destroy(id: int, db: Session = Depends(get_db)):
    return blog.destroy(id, db)


@router.put('/{id}', status_code=202)
def update(id, request: schema.Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db)


@router.get('/{id}', response_model=schema.ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    return blog.show(id, db)
