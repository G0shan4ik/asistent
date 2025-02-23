from .include import (
    User, PasswordStatus, BaseDatabaseDep, UserCreate, UserUpdatePassword, UserResponse,
    Optional, update, select, insert,
    getenv, logger
)


class UserManager(BaseDatabaseDep):
    async def create_user(self, user: UserCreate) -> int:
        _user: Optional[User] = await self.get_user_by_id(user_id=user.id)
        if _user:
            if getenv("DEBUG", None):
                logger.warning(f'USER (user_id == {str(user.id)[:-3]}***) already exists')

            return _user.id

        stmt = insert(User).values(
            id = user.id,
            username = user.username
        ).returning(User.id)

        result = (await self.session.execute(stmt)).scalar()
        await self.session.commit()

        if getenv("DEBUG", None):
            logger.success(f'SUCCESS created USER (user_id == {str(result)[:-3]}***)')

        return result

    async def get_user_by_id(self, user_id) -> Optional[User]:
        stmt = select(User).where(
            User.id == user_id
        )

        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def get_all_users(self) -> list[UserResponse]:
        result = await self.session.execute(select(User))
        users = result.scalars().all()

        return [UserResponse.from_orm(user) for user in users]

    async def set_or_update_password(self, user: UserUpdatePassword) -> Optional[UserUpdatePassword]:
        _user: Optional[User] = await self.get_user_by_id(user_id=user.id)
        if _user:
            __flag = True if _user.password else False
            stmt = (
                update(User)
                .where(User.id == user.id)
                .values(password=user.password)
            )
            await self.session.execute(stmt)
            await self.session.commit()

            if getenv("DEBUG", None):
                logger.info(
                    f'The password {"HAS BEEN UPDATED" if __flag else "IS SET"} '
                    f'for the user (user_id == {str(user.id)[:-3]}***)'
                )

            return PasswordStatus.UPDATE.value if __flag else PasswordStatus.CREATE.value

    async def check_user_password(self, user_id: int, check_password: str) -> bool:
        _user: Optional[User] = await self.get_user_by_id(user_id=user_id)
        if _user:
            stmt = select(User).where(
                User.id == user_id,
                User.password == check_password
            )
            return True if (await self.session.execute(stmt)).scalar_one_or_none() else False
        return False


__all__ = [
    "UserManager"
]