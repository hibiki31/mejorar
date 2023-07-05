import uvicorn

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_camelcase import CamelModel

from sqlalchemy.orm import Session

from log import setup_logger
from database import get_db
from settings import API_VERSION


import routers


logger = setup_logger(__name__)


tags_metadata = [
    {"name": "auth", "description": ""},
    {"name": "user", "description": ""},
]

app = FastAPI(
    title="MejorarAPI",
    description="",
    version=API_VERSION,
    openapi_tags=tags_metadata,
    docs_url="/api",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Version(CamelModel):
    initialized: bool
    version: str



@app.get("/api/version", response_model=Version)
def get_version(
        db: Session = Depends(get_db)
    ):

    return {"initialized": True, "version": API_VERSION}


app.include_router(routers.auth)
app.include_router(routers.user)
app.include_router(routers.content)




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)