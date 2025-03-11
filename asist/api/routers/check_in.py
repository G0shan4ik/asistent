from asist.database.methods.check_in import CheckInManager
from .include import *
from asist.database.models import CheckIn


check_in_router = APIRouter(
    tags=['CheckIn']
)


@check_in_router.post(
    '/check_in/create',
    response_model=CreatedModel
)
async def create_check_in(
    check_in_id: CreateCheckIn,
    check_in_db: Annotated[CheckInManager, Depends(sql_helper_factory(CheckInManager))]
):
    created_id: int = await check_in_db.create_check_in(check_in_id)
    return {
        'created_id': created_id
    }


@check_in_router.post(
    '/check_in/update_check_in'
)
async def update_check_in(
    check_in_id: int,
    data: UpdateCheckIn,
    check_in_db: Annotated[CheckInManager, Depends(sql_helper_factory(CheckInManager))]
):
    status: bool = await check_in_db.update_check_in(check_in_id, **data.model_dump(exclude_unset=True))

    return {
        'status': status
    }


@check_in_router.post(
    '/check_in/delete'
)
async def delete_check_in(
    check_in_id: int,
    check_in_db: Annotated[CheckInManager, Depends(sql_helper_factory(CheckInManager))]
):
    status: bool = await check_in_db.delete_check_in(check_in_id)
    return {
        "status": status
    }



@check_in_router.get(
    '/check_in/get_check_in',
    response_model=CheckInResponse
)
async def get_check_in(
    check_in_id: int,
    check_in_db: Annotated[CheckInManager, Depends(sql_helper_factory(CheckInManager))]
):
    _check_in: Optional[CheckIn] = await check_in_db.get_check_in_by_id(check_in_id)
    return {
        'id': _check_in.id,
        'check_in_name': _check_in.check_in_name,
        'dict_with_dates': _check_in.dict_with_dates,
        'user_id': _check_in.user_id,
    }


@check_in_router.get(
    '/check_in/get_all_user_check_in',
    response_model=list[CheckInResponse]
)
async def get_all_user_finances(
    user_id: int,
    check_in_db: Annotated[CheckInManager, Depends(sql_helper_factory(CheckInManager))]
):
    result: list[CheckInResponse] = await check_in_db.get_all_user_check_in(user_id=user_id)
    return result

