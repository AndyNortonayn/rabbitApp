from src.task.shemas import OutTaskModel
from src.task.db_operations import get_all_task, get_task_done,get_task_by_id, create_task_done, update_user_balance
from model import async_session
import requests
import httpx



async def check_user(user_id, chat_id):
    print(chat_id)
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember"
    params = {
        "chat_id": chat_id,
        "user_id": user_id
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Проверяем на ошибки HTTP
            data = response.json()
            if data['result']['status'] == 'member':
                print(data['result']['status'])
                return True  # Возвращаем информацию о пользователе

            return False
            
    except httpx.HTTPStatusError as e:
        print(f"Error response: {e.response.text}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


class TaskService():

    @classmethod
    async def get_valid_tasks(cls, user_id):
        tasks = await get_all_task(async_session)
        result = []
        for task in tasks:
            if task.validate == 1:
                answer = {'id': task.id, 'name': task.name, 'amount': task.amount, "done": await get_task_done(async_session, user_id, task.id), 'url': task.url}
                result.append(OutTaskModel(**answer))
        return result

    @classmethod
    async def get_tasks(cls, user_id):
        tasks = await get_all_task(async_session)
        result = []
        for task in tasks:

            answer = {'id': task.id, 'name': task.name, 'amount': task.amount,
                      "done": await get_task_done(async_session, user_id, task.id), 'url': task.url}
            result.append(OutTaskModel(**answer))
        return result

    @classmethod
    async def check_task(cls, user_id, task_id):
        task = await get_task_by_id(task_id)

        if task.validate == 0:
            print(0)
            await create_task_done(task.id, user_id)
            await update_user_balance(user_id, task.amount, task.amount)
            return await get_all_task(user_id)

        if task.validate == 1:
            print('checkkkkk')
            if await check_user(user_id, task.tg_id):
                await create_task_done(task.id, user_id)
                await update_user_balance(user_id, task.amount, task.amount)
                return await get_all_task(user_id)


