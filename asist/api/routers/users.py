from asist.database.methods.user import UserManager
from .include import *
from asist.database.models import User


user_router = APIRouter(
    tags=['Users']
)


@user_router.post(
    '/user/create',
    response_model=CreatedModel
)
async def create_account(
    user: UserCreate,
    user_db: Annotated[UserManager, Depends(sql_helper_factory(UserManager))]
):
    created_id: int = await user_db.create_user(user)
    return {
        'created_id': created_id
    }

@user_router.post(
    '/user/change_password'
)
async def change_password(
    user: UserUpdatePassword,
    user_db: Annotated[UserManager, Depends(sql_helper_factory(UserManager))]
):
    status: UserUpdatePassword = await user_db.set_or_update_password(user)

    return {
        'status': status
    }


@user_router.get(
    '/user/get_user',
    response_model=UserCreate
)
async def get_user(
    user_id: int,
    user_db: Annotated[UserManager, Depends(sql_helper_factory(UserManager))]
):
    _user: User = await user_db.get_user_by_id(user_id)
    return {
        'id': _user.id,
        'username': _user.username,
        'password': _user.password,
        'created_at': _user.created_at
    }


@user_router.get(
    '/user/get_all_users',
    response_model=list[UserResponse]
)
async def get_all_users(
    user_db: Annotated[UserManager, Depends(sql_helper_factory(UserManager))]
):
    _users: list[UserResponse] = await user_db.get_all_users()
    return _users


@user_router.get(
    '/user/check_password'
)
async def check_password(
    user_id: int,
    check_pass: str,
    user_db: Annotated[UserManager, Depends(sql_helper_factory(UserManager))]
):
    result: bool = await user_db.check_user_password(user_id=user_id, check_password=check_pass)
    return {"status": result}

