FROM python:3.13-slim

WORKDIR /app

# Системные зависимости для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости без создания виртуального окружения внутри контейнера
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем остальной код бэкенда
COPY . .

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]