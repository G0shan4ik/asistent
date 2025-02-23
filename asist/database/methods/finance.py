from .include import (
    Finance, BaseDatabaseDep, CreateFinance, FinanceResponse,
    Optional, update, select, insert, delete,
    getenv, logger
)


class FinanceManager(BaseDatabaseDep):
    async def create_finance(self, finance: CreateFinance) -> int:
        stmt = insert(Finance).values(
            source_name = finance.source_name,
            amount = finance.amount,
            description = finance.description,
            added_at = finance.added_at,
            user_id = finance.user_id
        ).returning(Finance.id)

        result = (await self.session.execute(stmt)).scalar_one_or_none()
        await self.session.commit()

        if getenv("DEBUG", None):
            logger.info(f'Create Finance for user (user_id == {finance.user_id})')

        return result

    async def get_finance_by_id(self, finance_id: int) -> Optional[Finance]:
        stmt = select(Finance).where(
            Finance.id == finance_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def update_finance(self, finance_id: int, **data: dict) -> bool:
        if self.get_finance_by_id(finance_id):
            allowed_fields = {
                "source_name",
                "amount",
                "description",
                "added_at",
            }
            update_data = {k: v for k, v in data.items() if k in allowed_fields}
            if not update_data:
                if getenv("DEBUG", None):
                    logger.error(f'Error update Finance (update_data is None) (finance_id == {finance_id})')
                return False

            stmt = (
                update(Finance)
                .where(Finance.id == finance_id)
                .values(**update_data)
            )
            await self.session.execute(stmt)
            await self.session.commit()

            if getenv("DEBUG", None):
                logger.success(f'Success update Finance (finance_id == {finance_id})')

            return True

        if getenv("DEBUG", None):
            logger.error(f'Error Delete finance (NOT FOUND FINANCE by ID) (finance_id == {finance_id})')

        return False

    async def delete_finance(self, finance_id: int) -> bool:
        if self.get_finance_by_id(finance_id):
            stmt = delete(Finance).where(
                Finance.id == finance_id
            )
            await self.session.execute(stmt)
            await self.session.commit()

            if getenv("DEBUG", None):
                logger.info(f'Delete Finance (finance_id == {finance_id})')

            return True

        if getenv("DEBUG", None):
            logger.error(f'Error Delete finance (NOT FOUND FINANCE by ID) (finance_id == {finance_id})')

        return False

    async def get_all_user_finances(self, user_id: int) -> list[FinanceResponse]:
        stmt = select(Finance).where(
            Finance.user_id == user_id
        )
        result = await self.session.execute(stmt)
        finances = result.scalars().all()

        return [FinanceResponse.from_orm(finance) for finance in finances]


__all__ = [
    "FinanceManager"
]