from fastapi import  APIRouter
from src.startButton.service import StartButtonService
from src.startButton.shemas import StartButtonModels

router = APIRouter()
start_button = StartButtonService()
@router.post("")
async def add_user (data: StartButtonModels.InStartModel):
    try:
        print(data)
        return await start_button.create_user(data)
    except:
        return {'error': 'this user already created'}


