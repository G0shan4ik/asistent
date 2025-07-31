from asist.database.methods.debts import DebtsManager
from .include import *
from asist.database.models import Debts


debts_router = APIRouter(
    tags=['Debts']
)


@debts_router.post(
    '/debts/create',
    response_model=CreatedModel
)
async def create_debts(
    debts_id: DebtsCreate,
    debts_db: Annotated[DebtsManager, Depends(sql_helper_factory(DebtsManager))]
):
    created_id: int = await debts_db.create_debts(debts_id)
    return {
        'created_id': created_id
    }


@debts_router.post(
    '/debts/update_debts'
)
async def update_debts(
    debts_id: int,
    data: DebtsUpdate,
    debts_db: Annotated[DebtsManager, Depends(sql_helper_factory(DebtsManager))]
):
    status: bool = await debts_db.update_debts(debts_id, **data.model_dump(exclude_unset=True))

    return {
        'status': status
    }


@debts_router.post(
    '/debts/delete'
)
async def delete_debts(
    debts_id: int,
    debts_db: Annotated[DebtsManager, Depends(sql_helper_factory(DebtsManager))]
):
    status: bool = await debts_db.delete_debts(debts_id)
    return {
        "status": status
    }



@debts_router.get(
    '/debts/get_debts',
    response_model=Optional[DebtsCreate]
)
async def get_debts(
    debts_id: int,
    debts_db: Annotated[DebtsManager, Depends(sql_helper_factory(DebtsManager))]
):
    _debts: Debts = await debts_db.get_debts_by_id(debts_id)
    return {
        "id": _debts.id,
        "title": _debts.title,
        "amount": _debts.amount,
        "paid": _debts.paid,
        "priority": _debts.priority,
        "due_date": _debts.due_date,
        "is_closed": _debts.is_closed,
        "notes": _debts.notes,
        "created_at": _debts.created_at,
        "user_id": _debts.user_id
    } if _debts else {}


@debts_router.get(
    '/debts/get_all_user_debts',
    response_model=Optional[list[DebtsResponse]]
)
async def get_all_user_debts(
    user_id: int,
    debts_db: Annotated[DebtsManager, Depends(sql_helper_factory(DebtsManager))]
):
    result: list[DebtsResponse] = await debts_db.get_all_user_debts(user_id=user_id)

    return result if result else []


@debts_router.get(
    '/debts/sort_user_debts_by_priority',
    response_model=Optional[list[DebtsResponse]]
)
async def get_all_user_debts(
    user_id: int,
    priority: PriorityStatus,
    debts_db: Annotated[DebtsManager, Depends(sql_helper_factory(DebtsManager))]
):
    result: list[DebtsResponse] = await debts_db.sort_user_debts_by_priority(
        user_id=user_id,
        priority=priority
    )

    return result if result else []

