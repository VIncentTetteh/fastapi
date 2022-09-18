from random import randrange
from turtle import title
from typing import List
from fastapi import FastAPI,status,HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine,get_db 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()






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

 
@app.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.PostCreate, db:Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *; """,
    # (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # con.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db:Session = Depends(get_db)): 
    # cursor.execute("""SELECT * FROM posts; """)
    # posts =  cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/latest")
def get_latest_post():
    post = my_post[len(my_post) -1]
    return {"post":post}


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id:int,db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s; """,(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)))
    # post = cursor.fetchone()
    # con.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return {"message","post successfully deleted"}


def find_post_index(id:int):
    for index,post in enumerate(my_post):
       if index == id:
        return index


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",
    # (post.title,post.content,post.published,str(id)))
    # post_to_update = cursor.fetchone()
    # con.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()

    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_post[post_to_update] = post_dict
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




