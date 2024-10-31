from pydantic import BaseModel


class OutReferal(BaseModel):
    nick_name: str
    point: int