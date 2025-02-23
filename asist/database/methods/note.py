from .include import (
    Note, BaseDatabaseDep, CreateNote,
    Optional, select, insert, delete, update,
    getenv, logger
)


class NoteManager(BaseDatabaseDep):
    async def create_note(self, note: CreateNote) -> int:
        stmt = insert(Note).values(
            note_name=note.note_name,
            description=note.description,
            image=note.image,
            copy_teg=note.copy_teg,
            user_id=note.user_id
        ).returning(Note.id)
        result = (await self.session.execute(stmt)).scalar()
        await self.session.commit()

        if getenv("DEBUG", False):
            logger.success(f'Create note for user (user_id == {note.user_id})')

        return result

    async def get_note_by_id(self, note_id: int) -> Optional[Note]:
        stmt = select(Note).where(
            Note.id == note_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def update_finance(self, note_id: int, **data: dict) -> bool:
        if self.get_note_by_id(note_id):
            allowed_fields = {
                "note_name",
                "image",
                "description",
                "copy_teg",
            }
            update_data = {k: v for k, v in data.items() if k in allowed_fields}
            if not update_data:
                if getenv("DEBUG", None):
                    logger.error(f'Error update Note (update_data is None) (note_id == {note_id})')
                return False

            stmt = (
                update(Note)
                .where(Note.id == note_id)
                .values(**update_data)
            )
            await self.session.execute(stmt)
            await self.session.commit()

            if getenv("DEBUG", None):
                logger.success(f'Success update Note (note_id == {note_id})')

            return True

        if getenv("DEBUG", None):
            logger.error(f'Error Delete note (NOT FOUND NOTE by ID) (note_id == {note_id})')

        return False

    async def delete_note(self, note_id: int) -> bool:
        if self.get_note_by_id(note_id):
            stmt = delete(Note).where(
                Note.id == note_id
            )

            await self.session.execute(stmt)
            await self.session.commit()

            if getenv("DEBUG", None):
                logger.info(f'Success DELETED Note (note_id == {note_id})')

            return True

        if getenv("DEBUG", None):
            logger.error(f'Error Delete Note (NOT FOUND NOTE by ID) (note_id == {note_id})')

        return False

    async def get_all_user_notes(self, user_id: int) -> [Note]:
        return (await self.session.execute(select(Note).where(Note.user_id == user_id))).scalars().all()


__all__ = [
    "NoteManager"
]