from aiohttp import ClientSession


class BaseClientManager:
    def __init__(self):
        self.session: ClientSession = None

    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.session.closed:
            await self.session.close()

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()


__all__ = [
    "BaseClientManager"
]