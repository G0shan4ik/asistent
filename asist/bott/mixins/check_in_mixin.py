from .include import BaseClientManager, getenv, Optional


class CheckInMixin(BaseClientManager):
    async def create_check_in(self, check_in_name: str, user_id: int) -> Optional[dict]:
        data = {
            "check_in_name": check_in_name,
            "user_id": user_id
        }
        async with self.session.post(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/check_in/create', json=data) as response:
            return await response.json()

    async def update_check_in(self, check_in_id: int, data: dict) -> Optional[dict]:
        async with self.session.post(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/check_in/update_check_in?check_in_id={check_in_id}', json=data) as response:
            return await response.json()

    async def delete_check_in(self, check_in_id: int) -> Optional[dict]:
        async with self.session.post(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/check_in/delete?check_in_id={check_in_id}') as response:
            return await response.json()

    async def get_check_in_by_id(self, check_in_id: int) -> Optional[dict]:
        async with self.session.get(
                f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/check_in/get_check_in?check_in_id={check_in_id}') as response:
            return await response.json()

    async def get_all_user_check_in(self, user_id: int) -> Optional[dict]:
        async with self.session.get(
                f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/check_in/get_all_user_check_in?user_id={user_id}') as response:
            return await response.json()