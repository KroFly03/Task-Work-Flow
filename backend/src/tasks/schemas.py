from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.employees.schemas import EmployeeSchema
from src.tasks.models import StatusEnum


class TaskCreateSchema(BaseModel):
    name: str
    description: str
    employee_id: Optional[int] = None
    parent_id: Optional[int] = None
    deadline: Optional[datetime] = None


class TaskSchema(BaseModel):
    id: int
    name: str
    description: str
    status: StatusEnum
    employee: Optional[EmployeeSchema]
    parent: Optional['TaskSchema']
    deadline: Optional[datetime]


class ImportantTaskSchema(BaseModel):
    task: str
    employees: list[EmployeeSchema]
