import asyncio
from typing import Awaitable

import aiohttp

from .helpers import parsing_list


async def get_result_parser_kuf(name: str, url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data: list[dict] = await response.json()
            return {name: [data[0]['value0'], data[0]['value1']]}


async def update_courses() -> list[list[str]]:
    res_mass: list[Awaitable] = []

    for name_course, url in parsing_list.items():
        res_mass.append(get_result_parser_kuf(name=name_course, url=url))

    return await asyncio.gather(*res_mass)


