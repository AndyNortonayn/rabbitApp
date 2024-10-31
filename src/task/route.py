import json
from typing import List

from fastapi import Header, HTTPException, Depends, APIRouter, FastAPI
from src.task.service import TaskService
from src.task.shemas import OutTaskModel
from src.middleware.authMiddleware import AuthMiddleware
import httpx

router = APIRouter()
service = TaskService
auth = AuthMiddleware()


@router.get("/", response_model=List[OutTaskModel])
async def get_tasks(custom_header: str = Header(None)):
    print(custom_header)

    if not custom_header:
        raise HTTPException(status_code=400, detail="Custom header missing")

    user = await auth.safe_parse_webapp_init_data(TOKEN, custom_header, json.loads)

    user_id = user['user']['id']
    tasks = await service.get_tasks(user_id)
    return tasks


@router.patch('/{id_task}', response_model=List[OutTaskModel])
async def check_task(id_task: int, custom_header: str = Header(None)):
    print(custom_header)

    if not custom_header:
        raise HTTPException(status_code=400, detail="Custom header missing")

    user = await auth.safe_parse_webapp_init_data(TOKEN, custom_header, json.loads)

    user_id = user['user']['id']

    await service.check_task(user_id, id_task)

    tasks = await service.get_tasks(user_id)
    return tasks

@router.get('/valid', response_model=List[OutTaskModel])
async def get_valid( custom_header: str = Header(None)):
    print(custom_header)

    if not custom_header:
        raise HTTPException(status_code=400, detail="Custom header missing")

    user = await auth.safe_parse_webapp_init_data(TOKEN, custom_header, json.loads)

    user_id = user['user']['id']

    tasks = await service.get_valid_tasks(user_id)
    return tasks




    
