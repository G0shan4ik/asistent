import asyncio
from typing import Awaitable

import aiohttp

from .helpers import parsing_list, merge_dictionaries


async def pars_actual_courses(name: str, url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data: list[dict] = await response.json()
            return {name: [data[0]['value0'], data[0]['value1']]}


async def update_courses() -> dict:
    res_mass: list[Awaitable] = []

    for name_course, url in parsing_list.items():
        res_mass.append(pars_actual_courses(name=name_course, url=url))

    return merge_dictionaries(await asyncio.gather(*res_mass))
