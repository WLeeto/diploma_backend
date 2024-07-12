FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Обновление и установка зависимостей
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

WORKDIR /app

# Копирование requirements.txt и установка зависимостей
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY . /app/

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
