from abc import ABC
from sqlalchemy.ext.asyncio import AsyncSession

from asist.database.models import *


class BaseDatabaseDep(ABC):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def close(self):
        await self.session.close()


__all__ = [
    "BaseDatabaseDep"
]