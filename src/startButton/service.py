from src.startButton.shemas import StartButtonModels
from src.startButton.db_operations import create_user, update_referal_balance
from model import async_session


class StartButtonService():
    async def create_user(self, user:StartButtonModels.InStartModel):
        try:
            session = async_session()
            new_user = await create_user(session, user)
            await session.close()
            if new_user:
                if user.referal_id:
                    return StartButtonModels.OutStartModel(id=new_user.id, nick_name=new_user.nick_name)
        except Exception as e:
            return {'error': str(e)}
