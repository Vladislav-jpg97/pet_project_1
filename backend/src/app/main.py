from fastapi import FastAPI

app = FastAPI(
    title="URL Shortener with Analytics",
    version="0.1.0",
    description="Сервис для быстрого сокращения ссылок с подробной аналитикой на FastAPI.",
)