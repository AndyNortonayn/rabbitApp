from model import User, Boost
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.startButton.shemas import StartButtonModels


async def create_user(db: AsyncSession, user: StartButtonModels.InStartModel):
    new_user = User(
        tg_id=user.user_id,
        nick_name=user.nick_name,
        avatar=user.avatar,
        referal_id=user.referal_id,
    )
    new_boost = Boost(
        tg_id=user.user_id,
        user=new_user
    )

    db.add(new_user)
    db.add(new_boost)

    try:
        await db.commit()
        await db.refresh(new_user)
        await db.refresh(new_boost)
        return new_user
    except Exception as exp:
        await db.rollback()
        raise exp

async def update_referal_balance(async_session: AsyncSession, user: StartButtonModels.InStartModel, amount = 5000):
    async with async_session() as session:
        query = select(User).where(User.tg_id == user.user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()


        if user:
            try:
                user.total_balance += amount
                user.amount_CRT += amount
                await session.commit()
                print("Update successful!")

            except Exception as e:
                print(f"Error occurred: {e}")
                await session.rollback()
        else:
            print(f"No user found for tg_id: {user.user_id}")