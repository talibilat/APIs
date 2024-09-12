from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import schemas, models
from ..database import get_db
from . import oauth2
from typing import List, Optional


# Create an APIRouter for posts with a common prefix and tag
router = APIRouter(
    prefix="/posts",  # All routes will start with '/posts'
    tags=['Posts']  # Group the routes under 'Posts' for documentation
)





@router.get("", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts




# Route to get a post by ID
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Retrieve a post by its ID"""
    retrieved_post = db.query(models.Post).filter(models.Post.id == id).first()  # Fetch the post with the given ID
    if not retrieved_post:  # If no post is found, raise a 404 error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id: {id} was not found'
        )
    return retrieved_post  # Return the retrieved post


# Route to create a new post
@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Create a new post"""
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())  # Create a new post instance with the provided data
    db.add(new_post)  # Add the new post to the database session
    db.commit()  # Commit the session to save the post
    db.refresh(new_post)  # Refresh the post object to get its updated state
    return new_post  # Return the newly created post


# Route to delete a post by ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Delete a post by its ID"""
    query_post = db.query(models.Post).filter(models.Post.id == id)# Find the post to delete
    deleted_post = query_post.first()
    if not deleted_post:  # If post is not found, raise a 404 error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {id} was not found'
        )
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform this action")
    
    db.delete(deleted_post)  # Delete the found post
    db.commit()  # Commit the session to save the changes
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # Return a 204 No Content response


# Route to update a post by ID
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Update a post by its ID"""
    query_post = db.query(models.Post).filter(models.Post.id == id)  # Find the post to update
    filtered_post = query_post.first()
    if filtered_post is None:  # If no post is found, raise a 404 error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID:{id} does not exist"
        )
    if filtered_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform this action")
    # Perform the update using the data provided in the request body
    query_post.update(post.model_dump(), synchronize_session=False)
    db.commit()  # Commit the session to save the changes

    # Fetch the updated post from the database
    updated_post = query_post.first()

    return updated_post  # Return the updated post




