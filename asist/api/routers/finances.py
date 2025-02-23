from asist.database.methods.finance import FinanceManager
from .include import *
from asist.database.models import Finance


finance_router = APIRouter(
    tags=['Finances']
)


@finance_router.post(
    '/finance/create',
    response_model=CreatedModel
)
async def create_finance(
    finance: CreateFinance,
    finance_db: Annotated[FinanceManager, Depends(sql_helper_factory(FinanceManager))]
):
    created_id: int = await finance_db.create_finance(finance)
    return {
        'created_id': created_id
    }


@finance_router.post(
    '/finance/update_finance'
)
async def update_finance(
    finance_id: int,
    data: UpdateFinance,
    finance_db: Annotated[FinanceManager, Depends(sql_helper_factory(FinanceManager))]
):
    status: bool = await finance_db.update_finance(finance_id, **data.model_dump(exclude_unset=True))

    return {
        'status': status
    }


@finance_router.post(
    '/finance/delete'
)
async def delete_finance(
    finance_id: int,
    finance_db: Annotated[FinanceManager, Depends(sql_helper_factory(FinanceManager))]
):
    status: bool = await finance_db.delete_finance(finance_id)
    return {
        "status": status
    }



@finance_router.get(
    '/finance/get_finance',
    response_model=CreateFinance
)
async def get_finance(
    finance_id: int,
    finance_db: Annotated[FinanceManager, Depends(sql_helper_factory(FinanceManager))]
):
    _finance: Optional[Finance] = await finance_db.get_finance_by_id(finance_id)
    return {
        'id': _finance.id,
        'source_name': _finance.source_name,
        'amount': _finance.amount,
        'description': _finance.description,
        'added_at': _finance.added_at,
        'user_id': _finance.user_id,
    }


@finance_router.get(
    '/finance/get_all_user_finances',
    response_model=list[FinanceResponse]
)
async def get_all_user_finances(
    user_id: int,
    finance_db: Annotated[FinanceManager, Depends(sql_helper_factory(FinanceManager))]
):
    result: list[FinanceResponse] = await finance_db.get_all_user_finances(user_id=user_id)
    return result

