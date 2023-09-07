from fastapi import FastAPI

from src.employees.routers import employee_router
from src.tasks.routers import task_router

app = FastAPI(debug=True)

app.include_router(employee_router)
app.include_router(task_router)
