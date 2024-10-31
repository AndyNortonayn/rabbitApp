import datetime
from typing import Optional, List

from pydantic import BaseModel, PositiveInt


class OutProfileModel(BaseModel):
        nick_name : str
        avatar : str
        amount_CRT : int
        amount_storage : int
        amount_garden : PositiveInt
        amount_ferm : PositiveInt
        wallet_adress: Optional[str] = None
        watering_bar : int
        last_watering: datetime.datetime
        claim_access: datetime.datetime
        nft_connected: List
        watering_ferm1: int
        watering_ferm2: int
        watering_ferm3: int
        clan_id : Optional[int] = None

class OutLeaderBoardModel (BaseModel):
        nick_name : str
        points : int
        avatar : str