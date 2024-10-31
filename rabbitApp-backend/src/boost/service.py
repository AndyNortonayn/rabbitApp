from datetime import datetime

from src.boost.db_operations import update_first_boost, update_second_boost,update_third_boost, update_third_boost,update_fourth_boost, select_boost, update_watering_amount
from fastapi import HTTPException
from model import async_session
from src.boost.shemas import OutBoostModel



class BoostService():
    async def _first_boost(self, user_id):
        await update_first_boost(user_id, 500,async_session)


    async def _second_boost(self, user_id):
        await update_second_boost(user_id, 500,async_session)

    async def _third_boost(self,user_id):
        await update_third_boost(user_id, 1000,async_session)

    async def _fourth_boost(self,user_id):
        await update_fourth_boost(user_id, 500,async_session)

    async def _check_watering_amount(self, boost):

        if boost.last_watering.strftime("%Y-%m-%d") != datetime.now().strftime("%Y-%m-%d"):
            await update_watering_amount(boost.tg_id, async_session)
            return 0

        return boost.watering_amount



    async def return_boost_list(self,user_id):
        boost = await select_boost(user_id, async_session)
        result={
            'id': boost.id,
            'auto_watering': boost.auto_watering,
            'garden': boost.garden,
            'amount_ferm': boost.amount_ferm,
            'watering_amount':await self._check_watering_amount(boost)
        }
        print(result)

        return OutBoostModel(**result)

    async def buy(self, user_id,id_boost):
        if id_boost == 1:
            await self._first_boost(user_id)
            return await self.return_boost_list(user_id)

        if id_boost == 2:
            await self._second_boost(user_id)
            return await self.return_boost_list(user_id)

        if id_boost == 3:
            await self._third_boost(user_id)
            return await self.return_boost_list(user_id)


        if id_boost == 4:
            await self._fourth_boost(user_id)
            return await self.return_boost_list(user_id)


        raise HTTPException(status_code=404, detail="Not Found Boost")
