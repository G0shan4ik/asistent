from .include import BaseClientManager, getenv, Optional


class UserMixin(BaseClientManager):
    async def create_user(self, user_id: int, user_name: Optional[str]) -> Optional[dict]:
        data = {
            "id": user_id,
            "username": user_name
        }

        async with self.session.post(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/user/create', json=data) as response:
            return await response.json()