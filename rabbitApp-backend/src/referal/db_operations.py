
from model import async_session, User

from sqlalchemy import select

async def get_referal(referal_id: int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(User).filter(User.referal_id == referal_id)
                .distinct(User.tg_id)
                .order_by(User.total_balance.desc())
            )
            users = result.scalars().all()
            return users










