from pydantic import BaseModel


class OutBoostModel(BaseModel):
    id: int
    auto_watering: int
    garden: int
    amount_ferm: int
    watering_amount: int