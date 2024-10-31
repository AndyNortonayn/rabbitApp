from model import User, Task, TaskDone, async_session
from sqlalchemy.future import select
from sqlalchemy import update

async def get_all_task(async_session):
    try:

        async with async_session() as session:
            async with session.begin():
                results = []
                result = await session.execute(select(Task))
                tasks = result.scalars().all()
                print(tasks)
                for task in tasks:
                    print(task)
                    results.append(task)
                print(results)
                return results

    except Exception as e:

        print(f"Error occurred: {e}")

async def get_task_done(async_session, tg_id, task_id):
    try:

        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(TaskDone).where((TaskDone.tg_id == tg_id) & (TaskDone.task_id == task_id))
                )
                users = result.scalars().all()
                if users:
                    return True
                return False
    except Exception as e:

        print(f"Error occurred: {e}")





async def get_task_by_id(task_id):
    async with async_session() as session:  # Создайте асинхронную сессию
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()  # Получите первый результат
        return task



async def create_task_done(task_id: int, tg_id: int):
    new_task_done = TaskDone(task_id=task_id, tg_id=tg_id)
    async with async_session() as session:
        session.add(new_task_done)
        await session.commit()
        await session.refresh(new_task_done)
    return new_task_done


async def get_user_by_tg_id( tg_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalars().first()
        return user


async def update_user_balance(tg_id: int, new_amount_CRT: int, new_total_balance: int):
    async with async_session() as session:
        async with session.begin():
            # Сначала получаем пользователя
            user = await get_user_by_tg_id(tg_id)

            # Теперь обновляем значения
            stmt = (
                update(User)
                .where(User.tg_id == tg_id)
                .values(amount_CRT=user.amount_CRT + new_amount_CRT, total_balance=user.total_balance + new_total_balance)
            )
            await session.execute(stmt)




