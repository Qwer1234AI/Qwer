# Используйте официальный образ Python
FROM python:3.8

# Установите рабочую директорию в /app
WORKDIR /app

# Скопируйте текущую директорию в /app внутри контейнера
COPY . /app

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запустите приложение при старте контейнера
CMD ["python", "qwer.py"]
