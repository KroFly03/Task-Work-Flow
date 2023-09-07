#!make
-include .env

makemigrations:
	poetry run alembic revision --autogenerate

migrate:
	poetry run alembic -x data=true upgrade head

start:
	poetry run python -m uvicorn src.main:app --reload
