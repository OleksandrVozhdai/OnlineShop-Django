FROM python:3.11-bullseye

ENV DEBIAN_FRONTEND=noninteractive

# Встановлення необхідних системних бібліотек
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    curl \
    gnupg2 \
    ca-certificates \
    apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

# Додавання репозиторію Microsoft
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg \
    && install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/ \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && rm microsoft.gpg

# Оновлення списку пакетів та встановлення драйвера ODBC
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
