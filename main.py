import json
from sys import prefix

import uvicorn
from fastapi import FastAPI,HTTPException

from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, HTMLResponse

from src.middleware.authMiddleware import AuthMiddleware
from src.startButton.route import router as startButtonRouter
from src.profile.route import router as profileRouter
from src.referal.route import router as refRouter
from src.clan.route import router as clanRouter
from src.boost.route import router as boostRouter
from src.task.route import router as taskRouter


auth = AuthMiddleware()
app = FastAPI()

class InitData(BaseModel):
    initData: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="../static"), name="static")

app.include_router(startButtonRouter, prefix='/startButton', tags=['startButton'])
app.include_router(profileRouter, prefix='/profile', tags=['profile'])
app.include_router(refRouter, prefix='/ref', tags=['ref'])
app.include_router(clanRouter, prefix='/clan', tags=['clan'])
app.include_router(boostRouter, prefix='/boost', tags=['boost'])
app.include_router(taskRouter, prefix='/task', tags=['task'])







if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="147.45.246.69",
        port=8001,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem",
        log_level="info",
    )
