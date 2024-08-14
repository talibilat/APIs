from random import randrange
from turtle import update
from typing import Optional
from certifi import contents
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from . import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost',database="fastapi",user='postgres',password="password123", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection Was Successfull!")
        break
    except Exception as error:
        print("Connection to the Database was failed")
        print("Error: ",error)
        time.sleep(5)




@app.get("/alchamy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data":posts}

@app.get("/posts")
def get_post(db : Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # returieved_post = cursor.fetchall()
    returieved_post = db.query(models.Post).all()
    return {"data": returieved_post}



@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db : Session = Depends(get_db)):
    # cursor.execute(
    #                 """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                 (post.title, post.content, post.published)
    #             )
    
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}



@app.get("/posts/{id}")
def get_post(id: int, response: Response, db : Session = Depends(get_db)):
    # cursor.execute(
    #                 """
    #                 SELECT *
    #                 FROM posts
    #                 WHERE id = %s
    #                 """,
    #                 (str(id)))
    # retrieved_post = cursor.fetchall()
    retrieved_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not retrieved_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    return{"post details": retrieved_post}



@app.delete('posts/{id}}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):
    # cursor.execute(
    #                 """
    #                 DELETE 
    #                 FROM posts
    #                 WHERE id=%s
    #                 RETURNING *
    #                 """,
    #                 (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).delete(models.Post.id == id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details = f'posr with id {id} was not found')
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put(("/posts/{id}"))
def update_post(id: int, post: schemas.PostCreate, db : Session = Depends(get_db)):
    # cursor.execute(
    #                 """
    #                 UPDATE posts
    #                 SET title = %s, content = %s, published = %s
    #                 WHERE id = %s
    #                 RETURNING *
    #                 """,
    #                 (post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    filtered_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post = filtered_post.update
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} does not exist")
    new = filtered_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return{"data": new}


