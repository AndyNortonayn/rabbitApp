from datetime import datetime, timedelta
from fastapi import HTTPException

from httpx import codes
from model import User, Boost,async_session
from sqlalchemy import select


async def update_first_boost(user_id: int, CRT: int,async_session):
    async with async_session() as session:
        result = await session.execute(
            select(User, Boost)
            .join(Boost, User.tg_id == Boost.tg_id)
            .filter(User.tg_id == user_id)
        )

        user_with_boost = result.first()
        if user_with_boost:
            user, boost = user_with_boost

            if boost.amount_ferm * 3 > boost.watering_amount:
                if user.amount_CRT >= CRT:


                    if boost.watering_amount < 3:
                        user.last_watering_ferm1 = datetime.now() - timedelta(hours=2)
                        boost.last_watering = datetime.now()
                    elif 3 <= boost.watering_amount < 6:
                        user.last_watering_ferm2 = datetime.now() - timedelta(hours=2)
                        boost.last_watering = datetime.now()
                    elif boost.watering_amount >= 6:
                        user.last_watering_ferm3 = datetime.now() - timedelta(hours=2)
                        boost.last_watering = datetime.now()

                    boost.watering_amount = boost.watering_amount + 1
                    user.amount_CRT -= CRT

                    await session.commit()
                else:
                    raise HTTPException(status_code=401, detail='Not Enouth CRT')
            else:
                raise HTTPException(status_code=401, detail='Time limit')
        else:
            print(f'User with tg_id {user_id} not found or has no boosts.')

async def update_third_boost(user_id: int, CRT, async_session):
    async with async_session() as session:
        result = await session.execute(
            select(User, Boost)
            .join(Boost, User.tg_id == Boost.tg_id)
            .filter(User.tg_id == user_id)
        )

        user_with_boost = result.first()
        if user_with_boost:
            user, boost = user_with_boost

            if user.amount_CRT >= CRT:
                boost_claim = datetime.now() - timedelta(days=2)
                user.last_claim_1 = boost_claim
                user.last_claim_2 = boost_claim
                user.last_claim_3 = boost_claim
                user.amount_CRT -= CRT

                await session.commit()

            else:
                raise HTTPException(status_code=401, detail='Not Enouth CRT')


async def update_fourth_boost(user_id: int, CRT, async_session):
    async with async_session() as session:
        result = await session.execute(
            select(User, Boost)
            .join(Boost, User.tg_id == Boost.tg_id)
            .filter(User.tg_id == user_id)
        )

        user_with_boost = result.first()
        if user_with_boost:
            user, boost = user_with_boost
            if boost.amount_ferm * 5 > boost.garden :
                if user.amount_CRT >= CRT:
                    boost.garden += 1
                    user.amount_CRT -= CRT

                    await session.commit()

                else:
                    raise HTTPException(status_code=401, detail='Not Enouth CRT')
            else:
                raise HTTPException(status_code=401, detail='No Access')

async def update_second_boost(user_id: int, CRT, async_session):

    async with async_session() as session:
        result = await session.execute(
            select(User, Boost)
            .join(Boost, User.tg_id == Boost.tg_id)
            .filter(User.tg_id == user_id)
        )

        user_with_boost = result.first()
        if user_with_boost:
            user, boost = user_with_boost
            if boost.auto_watering == 0 :
                if user.amount_CRT >= CRT:
                    boost.auto_watering = 1
                    user.amount_CRT -= CRT

                    await session.commit()

                else:
                    raise HTTPException(status_code=401, detail='Not Enouth CRT')
            else:
                raise HTTPException(status_code=401, detail='No Access')

async def select_boost (user_id: int, async_session):

    async with async_session() as session:
        result = await session.execute(
            select(User, Boost)
            .join(Boost, User.tg_id == Boost.tg_id)
            .filter(User.tg_id == user_id)
        )
        user_with_boost = result.first()
        if user_with_boost:
            user, boost = user_with_boost

            return boost

async def update_watering_amount(user_id: int, async_session):
    async with async_session() as session:
        result = await session.execute(
            select(User, Boost)
            .join(Boost, User.tg_id == Boost.tg_id)
            .filter(User.tg_id == user_id)
        )

        user_with_boost = result.first()
        if user_with_boost:
            user, boost = user_with_boost

            boost.watering_amount = 0
            await session.commit()

        return 0




