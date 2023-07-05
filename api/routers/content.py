from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Security
from sqlalchemy.orm import Session

from database import get_db
from log import setup_logger

from routers.auth import CurrentUser, get_current_user

from typing import List, Optional, Annotated

from schemas.content import *
from models.content import *


logger = setup_logger(__name__)
app = APIRouter(
    prefix="/api/content",
    tags=["content"],
)


@app.get("", response_model=List[GetContent])
def get_customer(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
    ):
    return db.query(Content).all()


@app.post("")
def post_api_users(
        current_user: Annotated[CurrentUser, Security(get_current_user, scopes=["write:content"])],
        request: PostContent,
        db: Session = Depends(get_db)
    ):


    if db.query(Content).filter(Content.title==request.title).one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="title duplicate"
        )
    
    add_model = Content(
        uuid = request.uuid,
        title = request.title
    )
    db.add(add_model)
    db.commit()

    return { "status": True }