FROM python:3.11-slim

# Устанавливаем системные библиотеки, необходимые для работы OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY . /app/

# Запуск приложения
CMD ["python", "app.py"]
