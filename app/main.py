from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        
        cursor = connection.cursor()
        print("Connection successful!")
        break
    except Exception:
        print("Connection unsuccessful!")
        time.sleep(30)

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_index(id):
    for i,post in enumerate(my_posts):
        if post["id"] == id:
            return i

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"This is a test"}

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * from posts""")
    posts = cursor.fetchall()
    return {"posts":posts}

@app.get("/posts/{id}")
async def get_post(id:int):
    cursor.execute("""SELECT * from posts WHERE id = %s""",(str(id)))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":f"Post with id:{id} is not present."})
    return {"post":post}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    post = cursor.fetchone()
    connection.commit()
    return {"post":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def del_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    post = cursor.fetchone()
    connection.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":f"Post with id:{id} is not present."})
    return {"post":post}

@app.put("/posts/{id}",status_code=status.HTTP_205_RESET_CONTENT)
async def updt_post(id:int,post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, str(id)))
    upt_post = cursor.fetchone()
    connection.commit()
    if upt_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":f"Post with id:{id} is not present."})
    return {"post":upt_post}