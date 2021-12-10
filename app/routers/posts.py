from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, Response, APIRouter

from app import oauth2
from ..database import get_db
from .. import schemas, models

router = APIRouter(prefix="/posts",tags=["Posts"])

@router.get("/",response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit:int = 10,skip:int = 0,search:Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}",response_model=schemas.Post)
async def get_post(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":f"Post with id:{id} is not present."})
    return post

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}")
async def del_post(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query= db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":f"Post with id:{id} is not present."})
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",status_code=status.HTTP_205_RESET_CONTENT,response_model=schemas.Post)
async def updt_post(id:int,updated_post:schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":f"Post with id:{id} is not present."})
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform requested action")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()