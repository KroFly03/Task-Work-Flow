from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_session
from src.tasks.schemas import TaskSchema, TaskCreateSchema, ImportantTaskSchema
from src.tasks.services import get_tasks_query, get_task_query, delete_task_query, update_task_query, create_task_query, \
    get_important_tasks_query

task_router = APIRouter(prefix='/tasks', tags=['Tasks'])


@task_router.get('', response_model=list[TaskSchema])
async def get_tasks(session: Session = Depends(get_session)):
    return await get_tasks_query(session)


@task_router.get('/important', response_model=list[ImportantTaskSchema])
async def get_important_tasks(session: Session = Depends(get_session)):
    return await get_important_tasks_query(session)


@task_router.post('', response_model=TaskSchema)
async def create_task(task: TaskCreateSchema, session: Session = Depends(get_session)):
    try:
        return await create_task_query(task, session)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@task_router.get('/{task_id}', response_model=TaskSchema)
async def get_task(task_id: int, session: Session = Depends(get_session)):
    try:
        return await get_task_query(task_id, session)
    except Exception as ex:
        raise HTTPException(status_code=404, detail='Not found.')


@task_router.delete('/{task_id}')
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    try:
        await delete_task_query(task_id, session)
        return {'message': 'Task deleted successfully.'}
    except Exception as ex:
        raise HTTPException(status_code=404, detail='Not found.')


@task_router.put('/{task_id}', response_model=TaskSchema)
async def update_task(task_id: int, task: TaskCreateSchema, session: Session = Depends(get_session)):
    try:
        return await update_task_query(task_id, task, session)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
