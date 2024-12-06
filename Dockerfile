# Используем официальный образ для Python (например, Python 3.9)
FROM python:3.9-slim


WORKDIR /code
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENV DATABASE_URL=sqlite:///data/todolist.db
RUN mkdir -p /data
CMD ["uvicorn", "app.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8080"]
