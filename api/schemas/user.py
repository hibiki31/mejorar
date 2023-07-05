from fastapi_camelcase import CamelModel
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class GetUser(CamelModel):
    username: str = Field(..., min_length=5)
    class Config:
        orm_mode = True

class PostUser(GetUser):
    password:str = Field(..., min_length=8)