
from fastapi import HTTPException
from src.clan.db_operations import get_clans_ordered_by_collected, get_users_by_clan_id, update_clan_id, create_clan,update_owner, delete_clan,update_clan_id_owner
from src.clan.shemas import OutClanModel, OutClanMemberModel
from model import async_session

class ClanService():
    ranks = {0: 'First_rank', 1000: 'Second_rank', 5000: 'Third_rank', }


    def __get_rank(self ,collected):
        if collected >= 0 and collected <= 1000:
            return self.ranks[1000]

        elif collected>= 1000 and collected <= 5000:
            return self.ranks[5000]

        elif collected>= 5000:
            return self.ranks[5000]


    async def get_all_clans(self):
        clans_array = []
        top = 0
        async with async_session() as session:
            clans = await get_clans_ordered_by_collected()
            for clan in clans:
                top+=1
                clans_array.append(OutClanModel(id=clan.id, name=clan.name, rank=self.__get_rank(clan.clan_collected),in_top=top, clan_balance=clan.clan_balance, clan_collacted = clan.clan_collected, amount_members= clan.amount_members, id_owner = clan.id_owner ))

            return clans_array


    async def get_clan_members(self, id):
        members = await get_users_by_clan_id(id)
        members_array = []

        for member in members:
            members_array.append(OutClanMemberModel(nick_name = member.nick_name, points= member.total_balance))

        return members_array

    async def get_clan(self, id):

        top = 0

        clans = await get_clans_ordered_by_collected()

        for clan in clans:
            top += 1

            if clan.id == id:
                amount_members_len = []
                amount_members = await get_users_by_clan_id(id)
                for i in amount_members:
                    amount_members_len.append(i)
                result = OutClanModel(id=clan.id, name=clan.name, rank=self.__get_rank(clan.clan_collected), in_top=top,
                             clan_balance=clan.clan_balance, clan_collacted=clan.clan_collected,
                             amount_members=len(amount_members_len), id_owner=int(clan.id_owner))

                return result


        raise HTTPException(status_code=404, detail='Clan not found')


    async def get_clan_byname(self, name):
        top = 0
        clans = await get_clans_ordered_by_collected()
        clans_array = []

        for clan in clans:
            top += 1

            if name in clan.name:
                amount_members_len = []
                amount_members = await get_users_by_clan_id(clan.id)
                for i in amount_members:
                    amount_members_len.append(i)
                result = OutClanModel(id=clan.id, name=clan.name, rank=self.__get_rank(clan.clan_collected), in_top=top,
                                      clan_balance=clan.clan_balance, clan_collacted=clan.clan_collected,
                                      amount_members=len(amount_members_len), id_owner=int(clan.id_owner))

                clans_array.append(result)

        if len(clans_array) > 0:
            return clans_array

        raise HTTPException(status_code=404, detail='Clan not found')


    async def invite(self, user_id, id_clan):
        async with async_session() as session:


            return await update_clan_id(id_clan, user_id)

    async def create_clans(self, user_id, name_clan):
        id_clan = await create_clan(name_clan, user_id)
        await self.invite(id_clan, user_id)
        await update_owner(user_id)
        return await self.get_clan(id_clan)

    async def delet_clan(self, id_clan):
        users = []
        user = await get_users_by_clan_id(id_clan)
        print(user, 'тест2')
        for i in user:
            users.append(i.nick_name)
        print(users, 'тест1')
        if len(users) == 0:
            await delete_clan(id_clan)
            for i in users:
                await update_clan_id_owner(i)

    async def invite_link(self, id_clan):
        return f'https://t.me/Grani_trening_bot?start=clan{id_clan}'







