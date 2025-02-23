from asist.database.methods.currency import CurrencyManager
from .include import *


currency_router = APIRouter(
    tags=['Currencies']
)


@currency_router.get(
    '/currency/get_or_create',
    response_model=CurrencyCreated
)
async def get_or_create_currency(
    curr_db: Annotated[CurrencyManager, Depends(sql_helper_factory(CurrencyManager))]
):
    data: CurrencyCreated = await curr_db.run_currency_update()
    return data

@currency_router.get(
    '/currency/select_currency',
    response_model=CurrencyCreated
)
async def select_currency(
    curr_db: Annotated[CurrencyManager, Depends(sql_helper_factory(CurrencyManager))]
):
    data: CurrencyCreated = await curr_db.select_curr_from_db()
    return data

