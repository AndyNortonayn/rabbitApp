import json

from fastapi import  Header, HTTPException, APIRouter
from src.middleware.authMiddleware import AuthMiddleware
from src.referal.service import ReferalService
from src.referal.shemas import OutReferal

router = APIRouter()
auth = AuthMiddleware()
sevice = ReferalService()


@router.get("", response_model=list[OutReferal])
async def get_all_referals( custom_header: str = Header(None)):
    if not custom_header:
        raise HTTPException(status_code=400, detail="Custom header missing")

    user = await auth.safe_parse_webapp_init_data(TOKEN, custom_header, json.loads)

    user_id = user['user']['id']

    return await sevice.get(user_id)