from typing import Optional

from pydantic import BaseModel, PositiveInt


class OutClanModel(BaseModel):
    id: int
    name: str
    rank: str
    in_top: int
    clan_balance: int
    clan_collacted: int
    amount_members: int
    id_owner: int



class OutClanMemberModel(BaseModel):
    nick_name: str
    points: int

