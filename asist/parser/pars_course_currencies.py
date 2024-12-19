import asyncio
from typing import Awaitable

import aiohttp

from .helpers import parsing_list, merge_dictionaries

from bs4 import BeautifulSoup
import lxml


async def pars_actual_courses(name: str, url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if 'https://bankibel.by/kursy-valut/evro/brest' == url:
                soup = BeautifulSoup(await response.text(), 'lxml')
                soup = soup.select_one('tbody').select('td.eur')
                return {name:
                    [
                        round(float(soup[0].text), 2),
                        round(float(soup[1].text), 2)
                    ]
                }

            data: list[dict] = await response.json()
            return {name:
                [
                    round(float(data[0]['value0']), 2),
                    round(float(data[0]['value1']), 2)
                ]
            }


async def update_courses() -> dict:
  res_mass: [Awaitable] = []

  for name_course, url in parsing_list.items():
    res_mass.append(pars_actual_courses(name=name_course, url=url))

  return merge_dictionaries(await asyncio.gather(*res_mass))
