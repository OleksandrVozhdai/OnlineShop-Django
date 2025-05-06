# Базовий образ із Python
FROM python:3.9

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо requirements.txt і встановлюємо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту в контейнер
COPY . .

# Виконуємо міграції (для тестів або запуску сервера)
RUN python manage.py makemigrations
RUN python manage.py migrate

# Команда за замовчуванням для запуску тестів
CMD ["python", "manage.py", "test", "main"]