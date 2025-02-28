from .. import models, schema
from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(db: Session, request: schema.Blog):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=404, detail='Blog does not exist')

    blog.delete(synchronize_session=False)
    db.commit()
    return blog


def update(id: int, request: schema.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=404, detail='Blog does not exist')

    blog.update(
        {"title": request.title,
         "body": request.body}, synchronize_session=False)
    db.commit()
    return "Updated Successfully"


def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail='Blog does not exist')
    return blog
