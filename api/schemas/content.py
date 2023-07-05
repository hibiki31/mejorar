from fastapi_camelcase import CamelModel
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, UUID4


class PostContent(CamelModel):
    title: str = Field(..., min_length=6)
    uuid: UUID4 = None
    class Config:
        orm_mode = True

class GetContent(PostContent):
    uuid: UUID4
    class Config:
        orm_mode = True