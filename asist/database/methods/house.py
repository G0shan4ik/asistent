from .include import (
    House, BaseDatabaseDep, HouseCreate,
    Optional, update, select, insert,
    getenv, logger, datetime, timedelta
)
from ...api.datamodels import HouseResponse


class HouseManager(BaseDatabaseDep):
    async def create_task(self, house: HouseCreate) -> int:
        stmt = insert(House).values(
            task_name=house.task_name,
            frequency=house.frequency,
            repeat=house.repeat,
            interval_days=house.interval_days,
            weekdays=house.weekdays,
            next_run_at=house.first_run or self._calculate_next_run(
                house.interval_days,
                house.weekdays
            ),
            is_active=True,
            user_id=house.user_id
        ).returning(House.id)

        result = (await self.session.execute(stmt)).scalar_one_or_none()
        await self.session.commit()

        if bool(getenv("DEBUG", False)):
            logger.info(f'Create House task for user (user_id == {house.user_id})')

        return result

    async def get_task_by_id(self, task_id: int) -> Optional[House]:
        stmt = select(House).where(
            House.id == task_id
        )

        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def get_all_tasks(self, user_id: int) -> list[HouseResponse]:
        stmt = select(House).where(
            House.user_id == user_id
        )
        result = await self.session.execute(stmt)
        houses = result.scalars().all()

        return [HouseResponse.from_orm(house) for house in houses]

    async def get_due_tasks(self) -> list[House]:
        now = datetime.utcnow()
        result = await self.session.execute(
            select(House).where(
                House.is_active == True,
                House.next_run_at != None,
                House.next_run_at <= now
            )
        )
        return result.scalars().all()

    async def update_task(
        self,
        task_id: int,
        **kwargs,
    ) -> Optional[House]:
        await self.session.execute(
            update(House)
            .where(House.id == task_id)
            .values(**kwargs)
        )
        await self.session.commit()
        return await self.get_task_by_id(task_id)

    async def deactivate_task(self, task_id: int) -> bool:
        task = await self.get_task_by_id(task_id)
        if not task:
            return False
        task.is_active = False
        await self.session.commit()
        return True

    async def schedule_next_run(self, task_id: int) -> Optional[House]:
        task = await self.get_task_by_id(task_id)
        if not task or not task.repeat:
            return None

        task.next_run_at = self._calculate_next_run(task.interval_days, task.weekdays)
        await self.session.commit()
        return task

    def _calculate_next_run(
        self,
        interval_days: Optional[int],
        weekdays: Optional[list[str]]
    ) -> Optional[datetime]:
        now = datetime.utcnow()

        if interval_days:
            return now + timedelta(days=interval_days)

        if weekdays:
            weekdays_map_en = {
                "monday": 0,
                "tuesday": 1,
                "wednesday": 2,
                "thursday": 3,
                "friday": 4,
                "saturday": 5,
                "sunday": 6,
            }
            weekdays_map_ru = {
                "monday": 0,
                "tuesday": 1,
                "wednesday": 2,
                "thursday": 3,
                "friday": 4,
                "saturday": 5,
                "sunday": 6,
            }
            today = now.weekday()
            upcoming_days = []

            upcoming_days_en = sorted(
                (weekdays_map_en[day.lower()] for day in weekdays if day.lower() in weekdays_map_en)
            )
            upcoming_days_ru = sorted(
                (weekdays_map_ru[day.lower()] for day in weekdays if day.lower() in weekdays_map_ru)
            )
            if upcoming_days_en:
                upcoming_days = upcoming_days_en
            elif upcoming_days_ru:
                upcoming_days = upcoming_days_ru

            for day in upcoming_days:
                if day > today:
                    return now + timedelta(days=day - today)
            # если не нашли позже в этой неделе — берем ближайший в следующей
            return now + timedelta(days=(7 - today + upcoming_days[0]))

        return None
