from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schema, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=201, tags=['Blogs'])
def create(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}', status_code=204, tags=['Blogs'])
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail='Blog does not exist')

    blog.delete(synchronize_session=False)
    db.commit()
    return blog


@app.put('/blog/{id}', status_code=202, tags=['Blogs'])
def update(id, request: schema.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=404, detail='Blog does not exist')
    blog.update(
        {"title": request.title, "body": request.body}, synchronize_session=False)

    db.commit()
    return "Updated Successfully"


@app.get('/blog', tags=['Blogs'])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{blog_id}', response_model=schema.ShowBlog, tags=['Blogs'])
def show(blog_id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Blog not found with id: {blog_id}"}
    return blog


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/user", response_model=schema.ShowUser, tags=['Users'])
def create_user(request: schema.User, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/user/{id}', response_model=schema.ShowUser, tags=['Users'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f'User with id:{id} does not exist')
    return user
