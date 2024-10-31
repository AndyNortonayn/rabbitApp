from typing import Optional

from pydantic import BaseModel, PositiveInt

class StartButtonModels():

    class InStartModel(BaseModel):
        user_id : PositiveInt
        nick_name : str
        avatar : Optional[str] = None
        referal_id : Optional[int] = None

    class OutStartModel(BaseModel):
        id : PositiveInt
        nick_name : str