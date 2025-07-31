from .include import BaseClientManager, getenv


class DebtsMixin(BaseClientManager):
    async def create_debts(self, data: dict) -> dict:
        async with self.session.post(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/debts/create', json=data) as response:
            return await response.json()

    async def update_debts(self, debts_id: int|str, data: dict) -> dict:
        async with self.session.post(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/debts/update_debts?debts_id={debts_id}', json=data) as response:
            return await response.json()

    async def delete_debts(self, debts_id: int|str) -> dict:
        async with self.session.post(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/debts/delete?debts_id={debts_id}') as response:
            return await response.json()

    async def get_debts_by_id(self, debts_id: int|str) -> dict:
        async with self.session.get(
                f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/debts/get_debts?debts_id={debts_id}') as response:
            return await response.json()

    async def get_all_user_debts(self, user_id: int|str) -> list[dict] | list:
        async with self.session.get(
                f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/debts/get_all_user_debts?user_id={user_id}') as response:
            return await response.json()

    async def sort_user_debts_by_priority(self, user_id: int|str, priority: str = 'low') -> dict:
        async with self.session.get(
                f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/debts/sort_user_debts_by_priority?user_id={user_id}&priority={priority}') as response:
            return await response.json()