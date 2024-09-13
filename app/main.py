from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body, Depends, FastAPI
from . import models
from .database import engine, get_db
from .router import post, user, auth, votes


models.Base.metadata.create_all(bind=engine)

origins = ["*"]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get('/')
def root():
    return {"message": "Hello, The App is running"}