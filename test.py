import aiohttp
from requests import get
from bs4 import BeautifulSoup
import lxml
import asyncio

async def pars():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://myfin.by/currency/usdrub/brest?conv_best_buy_eur=1112') as response:
            soup = BeautifulSoup(await response.text(encoding='utf-8'), 'lxml')
        print(soup.select_one('td.currencies-courses__currency-cell').text)
        # print(len(soup.select_one('div.k-top-currencies__item-body').select('div.course-brief-info__body')))


asyncio.run(pars())
# response = get(
#     'https://myfin.by/currency/usdrub/brest?conv_best_buy_eur=1112'
# )
# soup = BeautifulSoup(response.text, 'lxml')

# print(len(soup.select_one('div.k-top-currencies__item-body').select('div.course-brief-info__body')))