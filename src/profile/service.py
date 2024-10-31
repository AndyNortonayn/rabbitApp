import asyncio
from datetime import datetime, timedelta

from fastapi import HTTPException
from select import select
from model import async_session

from src.profile.db_operations import get_user_by_tg_id, get_watering_info, update_watering_info, update_wallet_address, update_balance_user, get_users_sorted_by_balance, update_referal_balances
from src.profile.shemas import OutProfileModel, OutLeaderBoardModel


def nft(wallet):
    return []

class ProfileHomeService:
    user, boost = None, None
    @classmethod
    async def udpate_wallet(cls, tg_id, wallet_number):
        await update_wallet_address(tg_id, wallet_number, async_session)

    @classmethod
    async def watering(cls, tg_id, ferm):
        async with async_session() as session:
            select_info = await get_watering_info(tg_id, session)
            print(select_info)

            if select_info:
                check = datetime.now() - select_info[0][int(ferm) - 1]
                if check >= timedelta(seconds=10):
                    await update_watering_info(tg_id, select_info[1][ferm - 1] + 1, datetime.now(), ferm)

                    return

                raise HTTPException(status_code=401, detail="Time limit")

            raise HTTPException(status_code=404, detail="Not Found")

    @classmethod
    async def create(cls, tg_id):
        instance = cls()
        user_and_boost = await get_user_by_tg_id(tg_id)
        instance.user, instance.boost= user_and_boost['user'], user_and_boost['boost']
        return instance

    def _check_auto_watering(self, number_ferm):
        if self.boost.auto_watering == 1:
            watering = {1: self.user.last_claim_1, 2: self.user.last_claim_2, 3: self.user.last_claim_3}
            for i in range(8):
                if datetime.now() - watering[number_ferm] >= timedelta(hours=3*(i+1)) and datetime.now() - watering[number_ferm] < timedelta(hours=3*(i+2)):
                    return i + 1
	
                elif datetime.now() - watering[number_ferm] > timedelta(hours=24):
                    return 8

        return 0

    def check_amount_storage(self, number_ferm: int, nft_garden: 0, ussual_amount: 10, boost_watering: 0.1):
        watering = {1: self.user.watering_ferm1, 2: self.user.watering_ferm2, 3: self.user.watering_ferm3}
        result = (10*self.boost.garden) * watering[number_ferm]

        return result

    def check_watering_bar(self, number_ferm: int):
        watering = {1: self.user.last_watering_ferm1, 2: self.user.last_watering_ferm2, 3: self.user.last_watering_ferm3}

        # Получение времени последнего полива
        datetime1 = watering[number_ferm]

        # Получение текущего времени без миллисекунд и секунд
        datetime2 = datetime.now()

        # Вычисление разницы во времени
        time_difference = datetime2 - datetime1

        # Перевод разницы во времени в секунды
        difference_in_seconds = time_difference.total_seconds()

        # Проверка, прошло ли более 60 секунд (1 минута)
        if difference_in_seconds < 20:
            # Вычисление процента времени от 0 до 100
            bar = 100 * difference_in_seconds
            result = int(bar / 20)
            if result < 0:
                return 0
            return result

        else:
            return 100

    def check_last_watering(self, ferm: int):
        watering = {1: self.user.last_watering_ferm1, 2: self.user.last_watering_ferm2, 3: self.user.last_watering_ferm3}
        result = timedelta(seconds=20)+watering[ferm]

        return result

    def check_claim_access(self, ferm):
        watering = {1: self.user.last_claim_1, 2: self.user.last_claim_2, 3: self.user.last_claim_3}
        result = timedelta(minutes=2) + watering[ferm]

        return result

    async def get_profile(self, number_ferm: int):
        if number_ferm <= self.boost.amount_ferm:
            data ={
                'nick_name': self.user.nick_name,
                'avatar': self.user.avatar,
                'amount_CRT': self.user.amount_CRT,
                'amount_storage': self.check_amount_storage(number_ferm,0,100,0.1) * (len(nft(self.user.wallet_adress))+1),
                'amount_ferm':self.boost.amount_ferm,
                'amount_garden':self.boost.garden,
                'wallet_adress': self.user.wallet_adress,
                'watering_bar': self.check_watering_bar(number_ferm),
                'last_watering': self.check_last_watering(number_ferm),
                'claim_access' : self.check_claim_access(number_ferm),
                'watering_ferm1': self.user.watering_ferm1,
                'watering_ferm2': self.user.watering_ferm2,
                'watering_ferm3': self.user.watering_ferm3,
                'nft_connected' : nft(self.user.wallet_adress),
                'clan_id': self.user.clan_id,
            }

            return OutProfileModel(**data)
        raise HTTPException(status_code=404, detail='Not Found')

    async def _referal_update_balance(self, amount_CRT):
        print('referals')
        if self.user.referal_id:
            print(self.user.referal_id)
            inreferal_id = await update_referal_balances(self.user.referal_id, amount_CRT*0.1)
            if inreferal_id:
                await update_referal_balances(inreferal_id*0.03)

    async def claim(self, tg_id,number_ferm: int):
        claim_array = {1: self.user.last_claim_1, 2: self.user.last_claim_2, 3: self.user.last_claim_3}
        if datetime.now() - claim_array[number_ferm] >= timedelta(minutes=2):
            print('test')
            profile = await self.get_profile(number_ferm)
            balance = await update_balance_user(tg_id, profile.amount_storage,number_ferm, async_session)
            profile.amount_CRT = balance
            await self._referal_update_balance(profile.amount_storage)
            return profile
        raise HTTPException(status_code=404, detail='Time limit')

    @classmethod
    async def get_leader_board(cls):
        try:
            all_users = []
            users = await get_users_sorted_by_balance(async_session)
            for user in users:
                all_users.append(OutLeaderBoardModel(nick_name= user.nick_name,  points= user.total_balance, avatar = user.avatar ))

            return all_users
        except Exception as e:
            print(e)
