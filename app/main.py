from random import randrange
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI,status,HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from . import models
from .database import engine,get_db 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool


while True:
    try:
        con = psycopg2.connect(host='localhost',database='fastapi',
        user='postgres',password='8462368', cursor_factory=RealDictCursor)
        cursor = con.cursor()
        print("database connected")
        break
    except Exception as error:
        print("connection to database failed")
        print("error",error)
        time.sleep(2)
        

my_post:List = [
    {"id":1,"title":"Fast API","content":"this is a fast api code"},
    {"id":2,"title":"CRUD API","content":"this is a CRUD api code"}
]

def find_post(id:int):
    for post in my_post:
        if post['id'] == id:
            return post

@app.get("/sql")
def test_post(db: Session = Depends(get_db)):
    return {"status","succuss"}
 
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *; """,
    (post.title,post.content,post.published))
    new_post = cursor.fetchone()
    con.commit()
    return {"data":new_post}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts; """)
    posts =  cursor.fetchall()
    return {"posts":posts}


@app.get("/posts/latest")
def get_latest_post():
    post = my_post[len(my_post) -1]
    return {"post":post}


@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s; """,(str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)))
    post = cursor.fetchone()
    con.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    return {"message","post successfully deleted"}


def find_post_index(id:int):
    for index,post in enumerate(my_post):
       if index == id:
        return index


@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",
    (post.title,post.content,post.published,str(id)))
    post_to_update = cursor.fetchone()
    con.commit()
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_post[post_to_update] = post_dict
    return post_to_update


