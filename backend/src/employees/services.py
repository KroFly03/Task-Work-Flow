from sqlalchemy import func
from sqlalchemy.orm import Session

from src.employees.models import EmployeeModel
from src.employees.schemas import EmployeeCreateSchema
from src.tasks.models import TaskModel


async def get_employees_query(session: Session):
    return session.query(EmployeeModel).all()


async def create_employee_query(data: EmployeeCreateSchema, session: Session):
    employee = EmployeeModel(**data.model_dump())
    session.add(employee)
    session.commit()
    return employee


async def get_employee_query(employee_id: int, session: Session):
    return session.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()


async def delete_employee_query(employee_id: int, session: Session):
    employee = session.query(EmployeeModel).filter(EmployeeModel.id == employee_id)

    if not employee.first():
        raise Exception

    employee.delete()
    session.commit()


async def update_employee_query(employee_id: int, data: EmployeeCreateSchema, session):
    employee = session.query(EmployeeModel).filter(EmployeeModel.id == employee_id)
    employee.update(data.model_dump())
    session.commit()
    return employee.first()


async def get_free_employee(session):
    subquery = (
        session.query(TaskModel.employee_id, func.count('*').label('count'))
        .filter(TaskModel.employee_id.isnot(None), TaskModel.status == 'todo')
        .group_by(TaskModel.employee_id)
        .subquery()
    )

    employee = (
        session.query(EmployeeModel)
        .join(subquery, EmployeeModel.id == subquery.c.employee_id)
        .order_by(subquery.c.count)
        .limit(1)
        .first()
    )

    return employee
