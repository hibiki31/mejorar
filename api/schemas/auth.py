from fastapi_camelcase import CamelModel
from typing import List, Optional
from pydantic import BaseModel


class TokenRFC6749Response(BaseModel):
    access_token: str
    token_type: str


class AuthValidate(TokenRFC6749Response):
    username: str