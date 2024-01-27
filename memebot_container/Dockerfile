# Использование официального образа Python как базового
FROM python:3.11-slim

# Установка рабочей директории в Docker-контейнере
WORKDIR /app

# Копирование файлов requirements.txt в рабочую директорию контейнера
COPY requirements.txt .

# Установка зависимостей из файла requirements.txt и очистка кэша pip
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов проекта в рабочую директорию контейнера
COPY . .

# Docker команда для запуска приложения
CMD ["python", "flask_app/main.py"]
