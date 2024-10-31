import json

from fastapi import Header, HTTPException, APIRouter, Query

from src.middleware.authMiddleware import AuthMiddleware
from src.clan.shemas import OutClanModel, OutClanMemberModel
from src.clan.service import ClanService

router = APIRouter()
sevice = ClanService()
auth = AuthMiddleware()


@router.get("", response_model=list[OutClanModel])
async def get_all_clan( ):
    return await sevice.get_all_clans()

@router.get("/{id_clan}", response_model=OutClanModel)
async def get_clan_by_id(id_clan: int):
    try:
        return await sevice.get_clan(id_clan)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="clan not found")

@router.get("/name/{name_clan}")
async def get_clans_by_name(name_clan: str):
    try:
        return await sevice.get_clan_byname(name_clan)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="clan not found")

@router.get("/members/{id_clan}", response_model=list[OutClanMemberModel])
async def get_members(id_clan: int):
    return await sevice.get_clan_members(id_clan)


@router.post("/{name_clan}")
async def create_clan(name_clan: str,custom_header: str = Header(None)):
    if not custom_header:
        raise HTTPException(status_code=400, detail="Custom header missing")

    user = await auth.safe_parse_webapp_init_data(TOKEN, custom_header, json.loads)

    user_id = user['user']['id']

    return await sevice.create_clans(user_id, name_clan)

@router.patch("/invite/")
async def invite(id_clan: int = Query(None)):
    return await sevice.invite_link(id_clan,)


@router.patch("/add_member/")
async def add_member(id_clan: int = Query(None), custom_header: str = Header(None)):
    if not custom_header:
        raise HTTPException(status_code=400, detail="Custom header missing")

    user = await auth.safe_parse_webapp_init_data(TOKEN, custom_header, json.loads)

    user_id = user['user']['id']
    await sevice.invite(id_clan, user_id)

    raise HTTPException(status_code=200, detail="Success update clan id")

@router.patch("/leave/")
async def leave_clan(custom_header: str = Header(None)):
    if not custom_header:
        raise HTTPException(status_code=400, detail="Custom header missing")

    user = await auth.safe_parse_webapp_init_data(TOKEN, custom_header, json.loads)

    user_id = user['user']['id']

    clan_id = await sevice.invite(None, user_id)
    print(clan_id)
    await sevice.delet_clan(clan_id)

    raise HTTPException(status_code=200, detail="Success leave")





