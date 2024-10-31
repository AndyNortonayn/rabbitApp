

from fastapi import Header, HTTPException, APIRouter, Query
from src.boost.service import BoostService
from src.middleware.authMiddleware import AuthMiddleware
from src.boost.shemas import OutBoostModel
import json

router = APIRouter()
srvice = BoostService()
auth = AuthMiddleware()



@router.get('/', response_model=OutBoostModel)
async def get_boost_list(custom_header: str = Header(None)):
    if not custom_header:
        raise HTTPException(status_code=400, detail="Custom header missing")

    user = await auth.safe_parse_webapp_init_data(TOKEN, custom_header, json.loads)
    user_id = user['user']['id']

    return await srvice.return_boost_list(user_id)

@router.patch("/{id_boost}/", response_model=OutBoostModel)
async def buy_boost(id_boost: int, custom_header: str = Header(None)):
    if not custom_header:
        raise HTTPException(status_code=400, detail="Custom header missing")

    user = await auth.safe_parse_webapp_init_data(TOKEN, custom_header, json.loads)
    user_id = user['user']['id']

    return await srvice.buy(user_id, id_boost)
