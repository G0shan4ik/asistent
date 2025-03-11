import aiohttp

from .include import (
    CurrencyExchangeRate, BaseDatabaseDep, CurrencyCreated,
    Optional, update, select, insert,
    getenv, logger
)
from .helpers import timer


class CurrencyManager(BaseDatabaseDep):
    URL = getenv('PARS_CURRENCY_URL')

    async def get_currency(self) -> CurrencyCreated:
        async with aiohttp.ClientSession() as aio_session:
            async with aio_session.get(self.URL) as response:
                if bool(getenv("DEBUG", False)):
                    logger.info(f'PARS_CURRENCY response status code == {response.status}')

                data = (await response.json())[0]

                return CurrencyCreated(
                    USD_in = float(data["USD_in"]), USD_out = float(data["USD_out"]),
                    EUR_in = float(data["EUR_in"]), EUR_out = float(data["EUR_out"]),
                    USD_RUB_in = float(data["USD_RUB_in"]), USD_RUB_out = float(data["USD_RUB_out"]),
                    RUB_EUR_in = float(data["RUB_EUR_in"]), RUB_EUR_out = float(data["RUB_EUR_out"]),
                    RUB_in = float(data["RUB_in"]), RUB_out = float(data["RUB_out"])
                )

    async def update_currency(self, currency: CurrencyCreated) -> CurrencyCreated:
        stmt1 = select(CurrencyExchangeRate.id)
        result: Optional[int] = (await self.session.execute(stmt1)).scalar_one_or_none()
        if result:
            stmt2 = update(CurrencyExchangeRate).where(
                CurrencyExchangeRate.id == result
            ).values(
                USD_in=currency.USD_in, USD_out=currency.USD_out,
                EUR_in=currency.EUR_in, EUR_out=currency.EUR_out,
                USD_RUB_in=currency.USD_RUB_in, USD_RUB_out=currency.USD_RUB_out,
                RUB_EUR_in=currency.RUB_EUR_in, RUB_EUR_out=currency.RUB_EUR_out,
                RUB_in=currency.RUB_in, RUB_out=currency.RUB_out
            )
            await self.session.execute(stmt2)
            await self.session.commit()

            if bool(getenv("DEBUG", False)):
                logger.success(f'CREATE CURRENCY')

            return currency
        else:
            stmt3 = insert(CurrencyExchangeRate).values(
                USD_in=currency.USD_in, USD_out=currency.USD_out,
                EUR_in=currency.EUR_in, EUR_out=currency.EUR_out,
                USD_RUB_in=currency.USD_RUB_in, USD_RUB_out=currency.USD_RUB_out,
                RUB_EUR_in=currency.RUB_EUR_in, RUB_EUR_out=currency.RUB_EUR_out,
                RUB_in=currency.RUB_in, RUB_out=currency.RUB_out
            )
            await self.session.execute(stmt3)
            await self.session.commit()

            if bool(getenv("DEBUG", False)):
                logger.success(f'UPDATE CURRENCY')

            return currency

    @timer
    async def run_currency_update(self) -> CurrencyCreated:
        if bool(getenv("DEBUG", False)):
            logger.info(f'Start PARS currency!')
        _currency: CurrencyCreated = await self.update_currency(await self.get_currency())
        return _currency

    async def select_curr_from_db(self) -> CurrencyCreated:
        stmt1 = select(CurrencyExchangeRate)
        result: Optional[CurrencyCreated] = (await self.session.execute(stmt1)).scalar_one_or_none()
        if result:
            return CurrencyCreated(
                USD_in=result.USD_in, USD_out=result.USD_out,
                EUR_in=result.EUR_in, EUR_out=result.EUR_out,
                USD_RUB_in=result.USD_RUB_in, USD_RUB_out=result.USD_RUB_out,
                RUB_EUR_in=result.RUB_EUR_in, RUB_EUR_out=result.RUB_EUR_out,
                RUB_in=result.RUB_in, RUB_out=result.RUB_out
            )
        else:
            return await self.run_currency_update()



__all__ = [
    "CurrencyManager"
]