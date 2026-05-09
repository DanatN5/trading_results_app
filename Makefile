install:
	uv sync

runserver:
	uvicorn app.main:app --host localhost --port 8000 --reload

lint:
	uv run ruff check

migarate:
	alembic upgrade head

up:
	docker compose up