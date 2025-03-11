from .include import BaseClientManager, getenv, Optional


class FinanceMixin(BaseClientManager):
    async def create_finance(self, source_name: str, user_id: int) -> Optional[dict]:
        data = {
            "source_name": source_name,
            "user_id": user_id
        }
        async with self.session.post(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/finance/create', json=data) as response:
            return await response.json()

    async def update_finance(self, data: dict) -> Optional[dict]:
        async with self.session.post(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/finance/update_finance', json=data) as response:
            return await response.json()

    async def delete_finance(self, finance_id: int) -> Optional[dict]:
        data = {
            'finance_id': finance_id
        }
        async with self.session.post(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/finance/delete', json=data) as response:
            return await response.json()

    async def get_finance(self, finance_id: int) -> Optional[dict]:
        data = {
            'finance_id': finance_id
        }
        async with self.session.post(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/finance/get_finance', json=data) as response:
            return await response.json()

    async def get_all_user_finances(self, user_id: int) -> Optional[dict]:
        data = {
            'user_id': user_id
        }
        async with self.session.post(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/finance/get_all_user_finances', json=data) as response:
            return await response.json()