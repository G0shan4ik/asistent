from .include import BaseClientManager, getenv, Optional


class CurrencyMixin(BaseClientManager):
    async def get_or_create_currency(self) -> None:
        async with self.session.get(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/currency/get_or_create') as response:
            return

    async def select_currency(self) -> dict:
        async with self.session.get(f'http://{getenv("API_HOST")}:{getenv("API_PORT")}/currency/select_currency') as response:
            return await response.json()