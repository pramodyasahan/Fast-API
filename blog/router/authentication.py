from blog.token import create_access_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from blog import schema, database, models
from blog.hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"],
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Incorrect email or password")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail="Incorrect email or password")

    access_token = create_access_token(
        data={"sub": user.email})

    return access_token
