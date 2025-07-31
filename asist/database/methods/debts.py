from .include import (
    Debts, BaseDatabaseDep, DebtsCreate, DebtsResponse, PriorityStatus,
    Optional, update, select, insert, delete,
    getenv, logger
)


class DebtsManager(BaseDatabaseDep):
    async def create_debts(self, debts: DebtsCreate) -> int:
        stmt = insert(Debts).values(
            title=debts.title,
            amount=debts.amount,
            priority=debts.priority,
            due_date=debts.due_date,
            notes=debts.notes,
            user_id=debts.user_id
        ).returning(Debts.id)

        result = (await self.session.execute(stmt)).scalar_one_or_none()
        await self.session.commit()

        if bool(getenv("DEBUG", False)):
            logger.info(f'Create Debts for user (user_id == {debts.user_id})')

        return result

    async def get_debts_by_id(self, debts_id: int) -> Optional[Debts]:
        stmt = select(Debts).where(
            Debts.id == debts_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def delete_debts(self, debts_id: int) -> bool:
        if self.get_debts_by_id(debts_id):
            stmt = delete(Debts).where(
                Debts.id == debts_id
            )

            await self.session.execute(stmt)
            await self.session.commit()

            if bool(getenv("DEBUG", False)):
                logger.info(f'Success DELETED Debts (debts_id == {debts_id})')

            return True

        if bool(getenv("DEBUG", False)):
            logger.error(f'Error Delete Debts (NOT FOUND Debts by ID) (debts_id == {debts_id})')

        return False

    async def update_debts(self, debts_id: int, **data: dict) -> bool:
        if self.get_debts_by_id(debts_id):
            allowed_fields = {
                "title",
                "amount",
                "paid",
                "priority",
                "due_date",
                "notes",
            }
            update_data = {k: v for k, v in data.items() if k in allowed_fields}
            if not update_data:
                if bool(getenv("DEBUG", False)):
                    logger.error(f'Error update CheckIn (update_data is None) (debts_id == {debts_id})')
                return False

            stmt = (
                update(Debts)
                .where(Debts.id == debts_id)
                .values(**update_data)
            )
            await self.session.execute(stmt)
            await self.session.commit()

            if bool(getenv("DEBUG", False)):
                logger.success(f'Success update Debts (debts_id == {debts_id})')

            return True

        if bool(getenv("DEBUG", False)):
            logger.error(f'Error UPDATE Debts (NOT FOUND Debts by ID) (debts_id == {debts_id})')

        return False

    async def get_all_user_debts(self, user_id: int) -> [DebtsResponse]:
        _debts = (await self.session.execute(
            select(Debts).where(Debts.user_id == user_id)
        )).scalars().all()

        return [DebtsResponse.from_orm(debt) for debt in _debts]

    async def sort_user_debts_by_priority(self, user_id: int, priority: PriorityStatus) -> [DebtsResponse]:
        _debts = (await self.session.execute(
            select(Debts).where(
                Debts.user_id == user_id
            ).where(Debts.priority == priority)
        )).scalars().all()

        return [DebtsResponse.from_orm(debt) for debt in _debts]