from pydantic import BaseModel


class EmployeeCreateSchema(BaseModel):
    name: str
    job: str


class EmployeeSchema(EmployeeCreateSchema):
    id: int
