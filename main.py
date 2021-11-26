from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None
    published: bool = True

my_posts = [
    {"title":"first post","content":"This is the first post","id":1},
    {"title":"second post","content":"This is the second post","id":2}
    ]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"This is a test"}

@app.get("/posts")
async def get_posts():
    return {"posts":my_posts}

@app.get("/posts/{id}")
async def get_post(id:int):
    post = find_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":f"Post with id:{id} is not present."})
    return {"post":post}

@app.post("/posts")
async def create_posts(post: Post):
    p = post.dict()
    p["id"] = randrange(0,100000)
    my_posts.append(p)
    return Response(status_code=status.HTTP_201_CREATED)