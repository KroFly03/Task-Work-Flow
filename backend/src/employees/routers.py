from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_session
from src.employees.schemas import EmployeeSchema, EmployeeCreateSchema
from src.employees.services import get_employees_query, create_employee_query, \
    delete_employee_query, update_employee_query, get_employee_query

employee_router = APIRouter(prefix='/employees', tags=['Employees'])


@employee_router.get('', response_model=list[EmployeeSchema])
async def get_employees(session: Session = Depends(get_session)):
    return await get_employees_query(session)


@employee_router.post('', response_model=EmployeeSchema)
async def create_employee(employee: EmployeeCreateSchema, session: Session = Depends(get_session)):
    try:
        return await create_employee_query(employee, session)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@employee_router.get('/{employee_id}', response_model=EmployeeSchema)
async def get_employee(employee_id: int, session: Session = Depends(get_session)):
    try:
        return await get_employee_query(employee_id, session)
    except Exception as ex:
        raise HTTPException(status_code=404, detail='Not found.')


@employee_router.delete('/{employee_id}')
async def delete_employee(employee_id: int, session: Session = Depends(get_session)):
    try:
        await delete_employee_query(employee_id, session)
        return {'message': 'Employee deleted successfully.'}
    except Exception as ex:
        raise HTTPException(status_code=404, detail='Not found.')


@employee_router.put('/{employee_id}', response_model=EmployeeSchema)
async def update_employee(employee_id: int, employee: EmployeeCreateSchema, session: Session = Depends(get_session)):
    try:
        return await update_employee_query(employee_id, employee, session)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
