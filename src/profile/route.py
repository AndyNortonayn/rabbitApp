import json
import os
from pprint import pprint
from typing import List

from fastapi import Header, HTTPException, Depends, APIRouter, FastAPI
from src.profile.service import ProfileHomeService
from src.profile.shemas import OutProfileModel, OutLeaderBoardModel
from src.middleware.authMiddleware import AuthMiddleware
from starlette.responses import JSONResponse, HTMLResponse


router = APIRouter()

auth = AuthMiddleware()


@router.get("/data", response_class=HTMLResponse)
async def read_html():
    try:
        print('sent html')
        with open("../static/index.html", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except UnicodeDecodeError as e:
        print(f"Ошибка декодирования: {e}")
        return JSONResponse(status_code=500, content={"message": "Ошибка при чтении файла."})

@router.get("/{number_ferm}", response_model=OutProfileModel)
async def read_items(number_ferm: int, custom_header: str = Header(None)):
    print(custom_header)
    try:
        if not custom_header:
            raise HTTPException(status_code=400, detail="Custom header missing")

        user = await auth.safe_parse_webapp_init_data(TOKEN, custom_header, json.loads)

        user_id = user['user']['id']

        profile_service = await ProfileHomeService.create(user_id)

        return await profile_service.get_profile(number_ferm)
    except Exception as e:
        print(e)


@router.get("/watering/{number_ferm}", response_model=OutProfileModel)
async def watering( number_ferm: int, custom_header: str = Header(None)):
        print(custom_header)
        if not custom_header:
            raise HTTPException(status_code=400, detail="Custom header missing")

        user = await auth.safe_parse_webapp_init_data(TOKEN, custom_header, json.loads)
        user_id = user['user']['id']
        print(number_ferm, 'number ferm')
        await ProfileHomeService.watering(user_id, number_ferm)

        profile_service = await ProfileHomeService.create(user_id)
        return await profile_service.get_profile(int(number_ferm))




@router.patch("/wallet/{wallet_number}", response_model=OutProfileModel)
async def watering( wallet_number: str, custom_header: str = Header(None)):
    try:
        if not custom_header:
            raise HTTPException(status_code=400, detail="Custom header missing")
        print('check1')
        user = await auth.safe_parse_webapp_init_data(TOKEN, custom_header, json.loads)
        user_id = user['user']['id']
        print(user_id, 'check')

        await ProfileHomeService.udpate_wallet(user_id, wallet_number,)

        profile_service = await ProfileHomeService.create(user_id)
        return await profile_service.get_profile(1)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/claim/{number_ferm}/', response_model=OutProfileModel)
async def claim(number_ferm: int, custom_header: str = Header(None)):
    if not custom_header:
        raise HTTPException(status_code=400, detail="Custom header missing")

    user = await auth.safe_parse_webapp_init_data(TOKEN, custom_header, json.loads)

    user_id = user['user']['id']

    profile_service = await ProfileHomeService.create(user_id)

    return await profile_service.claim(user_id,number_ferm)



@router.get('/leader_board/', response_model=List[OutLeaderBoardModel])
async def get_leader_board():

    return await ProfileHomeService.get_leader_board()


