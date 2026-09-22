dev:
	poetry run uvicorn src.app.main:app --reload

upgrade:
	poetry run alembic upgrade head

downgrade:
	poetry run alembic downgrade -1

build:
	docker compose up -d --build