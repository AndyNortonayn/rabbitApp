import asyncio
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import desc
from model import async_session, Clan, User


async def get_clans_ordered_by_collected():
    try:
        async with async_session() as session:
            result = await session.execute(
                select(Clan).order_by(desc(Clan.clan_collected))
            )
            clans = result.scalars().all()
        return clans
    except Exception as e:
        print(e)
        raise HTTPException


async def get_users_by_clan_id(clan_id: int):
    async with async_session() as session:
        async with session.begin():
            try:
                query = select(User).filter(User.clan_id == clan_id).order_by(User.total_balance.desc())
                result = await session.execute(query)
                users = result.scalars().all()
                return users
            except Exception as e:
                print(e)
                raise HTTPException(status_code=404, detail="clan not found")


async def update_clan_id(user_id: int, new_clan_id):
    async with async_session() as s:
        
        result = await s.execute(select(User).where(User.tg_id == user_id))
        user = result.scalars().first()

        if user:
            if user.owner == 1:
                return user.clan_id
            clan_id = user.clan_id
            user.clan_id = new_clan_id 
            await s.commit()
            print(f'Clan ID for user {user_id} updated to {new_clan_id}.')
            return clan_id
        else:
            print(f'User with tg_id {user_id} not found.')


async def update_clan_id_owner(user_id: int):
    async with async_session() as s:
        
        result = await s.execute(select(User).where(User.nick_name == user_id))
        user = result.scalars().first()

        if user:
            if user.owner == 1:

                user.clan_id = None 
                user.owner = 0
                await s.commit()




async def create_clan(name: str, id_owner: int):
    try:
        async with async_session() as session:
            new_clan = Clan(
                name=name,
                id_owner=id_owner
            )

            session.add(new_clan)
            await session.commit()
            await session.refresh(new_clan)
            return new_clan.id
    except:
        raise HTTPException(status_code=401, detail="user already have chanel")


async def update_owner(user_id: int):
    async with async_session() as s:
        try:
            
            result = await s.execute(select(User).where(User.tg_id == user_id))
            user = result.scalars().first()

            if user:

                user.owner = 1  
                await s.commit()  
            else:
                print(f'User with tg_id {user_id} not found.')
        except Exception as e:
            print(e)

async def delete_clan(clan_id: int):
    async with async_session() as session:
        async with session.begin():
            
            clan_to_delete = await session.get(Clan, clan_id)
            
            if clan_to_delete:
                await session.delete(clan_to_delete)
                await session.commit()
                print(f"Клан с id {clan_id} успешно удалён.")
            else:
                print(f"Клан с id {clan_id} не найден.")




