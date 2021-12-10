from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false

from app import models, schemas
from app.oauth2 import create_access_token
from app.utils import verify_password
from .database import get_db

router = APIRouter(tags=["Authentication"])

@router.get("/login",response_model=schemas.Token)
async def get_login(user: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user_dtl = db.query(models.User).filter(models.User.email == user.username).first()
    if user_dtl == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    is_correct = verify_password(password=user.password,hashed_password=user_dtl.password)
    if is_correct == false:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    token = create_access_token(data={"user_id": user_dtl.id})
    return {"access_token": token,"token_type": "bearer"}