
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models
from .. database import get_db
from typing import List


router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("", response_model = List[schemas.Post])
def get_post(db : Session = Depends(get_db)):
    returieved_post = db.query(models.Post).all()
    return returieved_post


@router.get("/{id}", response_model = schemas.Post)
def get_post(id: int, response: Response, db : Session = Depends(get_db)):
    retrieved_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not retrieved_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    return retrieved_post


@router.post('', status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(post: schemas.PostCreate, db : Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete('/{id}}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):
    deleted_post = db.query(models.Post).delete(models.Post.id == id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details = f'posr with id {id} was not found')
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(("/{id}"), response_model = schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db : Session = Depends(get_db)):
    filtered_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post = filtered_post.update
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} does not exist")
    new = filtered_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return new


