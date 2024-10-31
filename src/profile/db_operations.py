import asyncio
from datetime import datetime, timedelta


from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


from sqlalchemy.ext.asyncio import AsyncSession

from model import User, Boost, Clan
from model import async_session
from sqlalchemy.future import select




async def get_user_by_tg_id(tg_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User, Boost)
            .join(Boost, User.tg_id == Boost.tg_id)
            .filter(User.tg_id == tg_id)
        )

        user_with_boost = result.first()
        if user_with_boost:
            user, boost = user_with_boost
            return {'user': user, 'boost': boost}
        return None


async def get_watering_info(tg_id: int, session: AsyncSession):
    query = select(User).where(User.tg_id == tg_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user:
        return [
            [user.last_watering_ferm1, user.last_watering_ferm2, user.last_watering_ferm3],
            [user.watering_ferm1, user.watering_ferm2, user.watering_ferm3]
        ]
    return None
def check_limit_watering(check):
    print(2)
    if check >= 24:
        print(1)
        raise HTTPException(status_code=401, detail="Limit watering")
    return True

async def update_watering_info(tg_id: int, new_watering_ferm: int, new_last_watering_ferm: datetime, ferm: int):
    async with async_session() as session:
        query = select(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()


        if user:
            try:
                if ferm == 1:
                    print(3)
                    check_limit_watering(user.watering_ferm1)
                    user.watering_ferm1 = new_watering_ferm
                    user.last_watering_ferm1 = new_last_watering_ferm
                elif ferm == 2:
                    check_limit_watering(user.watering_ferm2)
                    user.watering_ferm2 = new_watering_ferm
                    user.last_watering_ferm2 = new_last_watering_ferm
                elif ferm == 3:
                    check_limit_watering(user.watering_ferm3)
                    user.watering_ferm3 = new_watering_ferm
                    user.last_watering_ferm3 = new_last_watering_ferm

                await session.commit()
                print("Update successful!")

            except Exception as e:
                print(f"Error occurred: {e}")
                await session.rollback()
        else:
            print(f"No user found for tg_id: {tg_id}")

async def update_wallet_address(tg_id, wallet_number, async_session):
    async with async_session() as session:
        async with session.begin():
            user = await session.execute(
                select(User).where(User.tg_id == tg_id)
            )
            user = user.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            try:
                user.wallet_adress = wallet_number
                session.add(user)
                await session.commit()
                print(f"Updated wallet address for user {tg_id} to {wallet_number}.")
            except IntegrityError as e:
                print(e)
                await session.rollback()
                raise HTTPException(status_code=400, detail="Integrity error occurred")


async def update_balance_сlan(clan_id, points, async_session):
    async with async_session() as session:
        async with session.begin():
            user = await session.execute(
                select(Clan).where(Clan.id == clan_id)
            )
            user = user.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            try:
                user.clan_balance = user.clan_balance + points
                user.clan_collected = user.clan_collected +  points
                session.add(user)
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(status_code=400, detail="Integrity error occurred")


async def update_balance_user(tg_id,  amount_CRT, ferm,async_session):
    async with async_session() as session:
        async with session.begin():
            user = await session.execute(
                select(User).where(User.tg_id == tg_id)
            )
            user = user.scalar_one_or_none()
            if not user:

                raise HTTPException(status_code=404, detail="User not found")

            async def update_all_other(user, amount_CRT):
                if user.clan_id:
                    await update_balance_сlan(user.clan_id, int(amount_CRT*0.1), async_session)
                    dolia = 0.9
                else:
                    dolia= 1

                user.amount_CRT = user.amount_CRT + int(amount_CRT * dolia)
                user.total_balance = user.total_balance + int(amount_CRT * dolia)



            try:
                if ferm == 1:
                    user.last_watering_ferm1 = datetime.now() - timedelta(hours=24)
                    user.watering_ferm1 = 0
                    user.last_claim_1 = datetime.now()
                    await update_all_other(user, amount_CRT)
                elif ferm == 2:
                    user.last_watering_ferm2 = datetime.now() - timedelta(hours=24)
                    user.watering_ferm2 = 0
                    user.last_claim_2 = datetime.now()
                    await update_all_other(user, amount_CRT)
                elif ferm == 3:
                    user.last_watering_ferm3 = datetime.now() - timedelta(hours=24)
                    user.watering_ferm3 = 0
                    user.last_claim_3 = datetime.now()
                    await update_all_other(user, amount_CRT)

                balance = user.amount_CRT

                session.add(user)
                await session.commit()
                return balance
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(status_code=400, detail="Integrity error occurred")


async def get_users_sorted_by_balance(async_session: AsyncSession):
    try:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(User).order_by(User.total_balance.desc())
                )
                users = result.scalars().all()
                return users
    except Exception as e:

        print(f"Error occurred: {e}")



async def update_referal_balances(tg_id, amount_CRT):
    try:
        async with async_session() as session:
            async with session.begin():
                user = await session.execute(
                    select(User).where(User.tg_id == tg_id)
                )
                user = user.scalar_one_or_none()
                if not user:
                    raise HTTPException(status_code=404, detail="User not found")

                try:
                    user.amount_CRT += amount_CRT
                    user.total_balance += amount_CRT
                    session.add(user)
                    await session.commit()
                    return user.referal_id
                except IntegrityError as e:
                    await session.rollback()
                    raise HTTPException(status_code=400, detail="Integrity error occurred")
    except Exception as e:
        print('erorr', e)

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
