from pydantic import BaseModel

class OutTaskModel(BaseModel):
    id: int
    name: str
    amount: int
    done: bool
    url: str