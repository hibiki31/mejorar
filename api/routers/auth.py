import jwt
import secrets

from datetime import datetime, timedelta
from typing import Annotated
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Security, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from sqlalchemy.orm import Session

from log import setup_logger
from database import get_db, SessionLocal
from settings import *

from schemas.auth import TokenRFC6749Response, AuthValidate
from models import User


logger = setup_logger(__name__)


app = APIRouter(prefix="/api/auth")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scopes = {
        "write:user": "",
        "write:content": ""
    }
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth", 
    auto_error=False,
    scopes=oauth2_scopes
)


class CurrentUser(BaseModel):
    username: str
    token: str


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
        security_scopes: SecurityScopes, 
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session,Depends(get_db)]
    ) -> CurrentUser:
    # ヘッダーに必要なスコープ情報を格納し、通知する
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    if token == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not exist",
            headers={"WWW-Authenticate": authenticate_value}
        )

    # JWTトークンペイロードの検証
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature has expired",
            headers={"WWW-Authenticate": authenticate_value}
        )
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": authenticate_value}
        )
    
    try:
        db.query(User).filter(User.username==username).one()
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Illegal jwt",
            headers={"WWW-Authenticate": authenticate_value}
        )

    return CurrentUser(username=username, token=token)


@app.on_event("startup")
def startup_event():
    db = SessionLocal()

    if not db.query(User).all() == []:
        return

    admin_password = secrets.token_urlsafe(12)
    logger.info(f"admin : {admin_password}")
    
    user_model = User(
        username="admin", 
        hashed_password=get_password_hash(admin_password)
    )

    db.add(user_model)
    db.commit()


@app.post("", response_model=TokenRFC6749Response, tags=["auth"])
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(), 
        db: Session = Depends(get_db)
    ):

    try:
        user:User = db.query(User).filter(User.username==form_data.username).one()
    except:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    if not verify_password(plain_password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


    if form_data.scopes == []:
        scopes = list(oauth2_scopes.keys())
    else:
        scopes = form_data.scopes

    access_token = create_access_token(
        data={
            "sub": user.username,
            "scopes": scopes
            },
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@app.get("/validate", tags=["auth"], response_model=AuthValidate)
def read_auth_validate(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)
    ):

    user = db.query(User).filter(User.username==current_user.username).one()

    return {
        "access_token": current_user.token, 
        "username": current_user.username, 
        "token_type": "Bearer",
    }