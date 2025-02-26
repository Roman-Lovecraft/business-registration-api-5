# Используем официальный базовый образ Python
FROM python:3.9-slim

# Устанавливаем переменную окружения для пути проекта
ENV PROJECT_PATH=/app

# Устанавливаем зависимости для работы Chrome и ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libgconf-2-4 \
    gnupg \
    curl \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Установка Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Удаляем старую версию ChromeDriver, если она существует
RUN rm -f /usr/local/bin/chromedriver

# Установка ChromeDriver (ищем последнюю стабильную версию)
RUN wget -q -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/133.0.6943.53/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Устанавливаем рабочую директорию
WORKDIR $PROJECT_PATH

# Копируем файлы проекта
COPY . $PROJECT_PATH

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для uvicorn
EXPOSE 8000

# Команда для запуска API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

