from src.referal.shemas import OutReferal
from src.referal.db_operations import get_referal


class ReferalService():
    async def get(self, tg_id):
        referal_array = []
        referals = await get_referal(tg_id)

        for referal in referals:
            point = referal.total_balance * 0.1
            referal_array.append(OutReferal(nick_name = referal.nick_name, point = int(point)))


        return referal_array