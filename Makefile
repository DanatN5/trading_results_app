install:
	uv sync

runserver:
	uvicorn app.main:app --host localhost --port 8000 --reload

lint:
	uv run ruff check

migarate:
	alembic upgread head

up:
	docker compose up