from .include import (
    CheckIn, BaseDatabaseDep, CreateCheckIn,
    Optional, select, insert, delete, update,
    getenv, logger
)


class CheckInManager(BaseDatabaseDep):
    async def create_check_in(self, check_in: CreateCheckIn) -> int:
        stmt = insert(CheckIn).values(
            check_in_name=check_in.check_in_name,
            user_id=check_in.user_id
        ).returning(CheckIn.id)
        result = (await self.session.execute(stmt)).scalar()
        await self.session.commit()

        if getenv("DEBUG", False):
            logger.success(f'Create "check_in" for user (user_id == {check_in.user_id})')

        return result

    async def get_check_in_by_id(self, check_in_id: int) -> Optional[CheckIn]:
        stmt = select(CheckIn).where(
            CheckIn.id == int(check_in_id)
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def update_check_in(self, check_in_id: int, **data: dict) -> bool:
        if self.get_check_in_by_id(check_in_id):
            allowed_fields = {
                "check_in_name",
                "dict_with_dates",
            }
            update_data = {k: v for k, v in data.items() if k in allowed_fields}
            if not update_data:
                if bool(getenv("DEBUG", False)):
                    logger.error(f'Error update CheckIn (update_data is None) (check_in_id == {check_in_id})')
                return False

            stmt = (
                update(CheckIn)
                .where(CheckIn.id == check_in_id)
                .values(**update_data)
            )
            await self.session.execute(stmt)
            await self.session.commit()

            if bool(getenv("DEBUG", False)):
                logger.success(f'Success update CheckIn (check_in_id == {check_in_id})')

            return True

        if bool(getenv("DEBUG", False)):
            logger.error(f'Error Delete CheckIn (NOT FOUND CheckIn by ID) (check_in_id == {check_in_id})')

        return False

    async def delete_check_in(self, check_in_id: int) -> bool:
        if self.get_check_in_by_id(check_in_id):
            stmt = delete(CheckIn).where(
                CheckIn.id == check_in_id
            )

            await self.session.execute(stmt)
            await self.session.commit()

            if bool(getenv("DEBUG", False)):
                logger.info(f'Success DELETED CheckIn (check_in_id == {check_in_id})')

            return True

        if bool(getenv("DEBUG", False)):
            logger.error(f'Error Delete CheckIn (NOT FOUND CheckIn by ID) (check_in_id == {check_in_id})')

        return False

    async def get_all_user_check_in(self, user_id: int) -> [CheckIn]:
        return (await self.session.execute(
            select(CheckIn).where(CheckIn.user_id == user_id)
        )).scalars().all()


__all__ = [
    "CheckInManager"
]