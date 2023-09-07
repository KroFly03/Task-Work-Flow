from sqlalchemy.orm import Session

from src.employees.schemas import EmployeeSchema
from src.employees.services import get_free_employee
from src.tasks.models import TaskModel
from src.tasks.schemas import TaskCreateSchema, ImportantTaskSchema


async def get_tasks_query(session: Session):
    return session.query(TaskModel).all()


async def create_task_query(data: TaskCreateSchema, session: Session):
    task = TaskModel(**data.model_dump())
    session.add(task)
    session.commit()
    return task


async def get_task_query(task_id: int, session: Session):
    return session.query(TaskModel).filter(TaskModel.id == task_id).first()


async def delete_task_query(task_id: int, session: Session):
    task = session.query(TaskModel).filter(TaskModel.id == task_id)

    if not task.first():
        raise Exception

    task.delete()
    session.commit()


async def update_task_query(task_id: int, data: TaskCreateSchema, session):
    task = session.query(TaskModel).filter(TaskModel.id == task_id)
    task.update(data.model_dump())
    session.commit()
    return task.first()


async def get_important_tasks_query(session):
    important_tasks = session.query(TaskModel).filter(TaskModel.employee_id == None, TaskModel.parent_id != None).all()
    employee = await get_free_employee(session)

    return [
        ImportantTaskSchema(
            task=task.name,
            employees=[EmployeeSchema(**employee.__dict__)
            ],
        )
        for task in important_tasks
    ]
