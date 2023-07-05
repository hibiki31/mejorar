from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Security
from sqlalchemy.orm import Session

from database import get_db
from log import setup_logger

from routers.auth import CurrentUser, get_current_user, get_password_hash

from typing import List, Optional, Annotated

from schemas.user import *
from models.user import *


logger = setup_logger(__name__)
app = APIRouter(
    prefix="/api/user",
    tags=["user"],
)


@app.get("", response_model=List[GetUser])
def get_customer(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)
    ):
    return db.query(User).all()


@app.post("")
def post_api_users(
        current_user: Annotated[User, Security(get_current_user, scopes=["write:user"])],
        request: PostUser,
        db: Session = Depends(get_db)
    ):
    
    if db.query(User).filter(User.username==request.username).one_or_none():
        raise HTTPException(
            status_code=400,
            detail=""
        )

    # ユーザ追加
    user_model = User(
        username=request.username,
        hashed_password=get_password_hash(request.password)
    )
    db.add(user_model)
    db.commit()

    return { "status": True }