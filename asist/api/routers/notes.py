from asist.database.methods.note import NoteManager
from .include import *
from asist.database.models import Note


note_router = APIRouter(
    tags=['Notes']
)


@note_router.post(
    '/note/create',
    response_model=CreatedModel
)
async def create_note(
    note: CreateNote,
    note_db: Annotated[NoteManager, Depends(sql_helper_factory(NoteManager))]
):
    created_id: int = await note_db.create_note(note)
    return {
        'created_id': created_id
    }


@note_router.post(
    '/note/update_note'
)
async def update_note(
    note_id: int,
    data: UpdateNote,
    note_db: Annotated[NoteManager, Depends(sql_helper_factory(NoteManager))]
):
    status: bool = await note_db.update_finance(note_id, **data.model_dump(exclude_unset=True))

    return {
        'status': status
    }


@note_router.post(
    '/note/delete'
)
async def delete_note(
    note_id: int,
    note_db: Annotated[NoteManager, Depends(sql_helper_factory(NoteManager))]
):
    status: bool = await note_db.delete_note(note_id)
    return {
        "status": status
    }



@note_router.get(
    '/note/get_note',
    response_model=CreateNote
)
async def get_note(
    note_id: int,
    note_db: Annotated[NoteManager, Depends(sql_helper_factory(NoteManager))]
):
    _note: Optional[Note] = await note_db.get_note_by_id(note_id)
    return {
        'id': _note.id,
        'note_name': _note.note_name,
        'image': _note.image,
        'description': _note.description,
        'copy_teg': _note.copy_teg,
        'user_id': _note.user_id,
    }


@note_router.get(
    '/note/get_all_user_notes',
    response_model=list[NoteResponse]
)
async def get_all_user_finances(
    user_id: int,
    note_db: Annotated[NoteManager, Depends(sql_helper_factory(NoteManager))]
):
    result: list[NoteResponse] = await note_db.get_all_user_notes(user_id=user_id)
    return result

