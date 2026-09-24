dev:
	poetry run uvicorn src.app.main:app --reload

# Создать новую миграцию (автогенерация по моделям)
# Использование: make make-migration m="added user table"
make-migration:
	poetry run alembic revision --autogenerate -m "$(m)"

# Применить все новые миграции к базе данных
upgrade:
	poetry run alembic upgrade head

# Откатить последнюю миграцию
downgrade:
	poetry run alembic downgrade -1

# Собрать и запустить проект через Docker Compose (с пересборкой образов и обновлением томов при необходимости)
build:
	docker compose up -d --build

# Полный перезапуск базы данных и контейнеров с очисткой томов (помогает при сбросе паролей/ошибках БД)
dc-reset:
	docker compose down -v
	docker compose up -d