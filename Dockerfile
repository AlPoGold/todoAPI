
FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt

ENV DATABASE_URL=sqlite:///data/todolist.db
RUN mkdir -p /data
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
