# 1. Използване на официален лек Python имидж
FROM python:3.14

# 2. Настройка на работната директория
WORKDIR /app

# 3. Задаване на променливи за оптимизация на Python в контейнера
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Инсталиране на системни библиотеки, нужни за PostgreSQL (psycopg2) и компилация
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Копиране и инсталиране на зависимостите
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# 6. Копиране на кода на целия проект
COPY . /app/

# 7. Събиране на статичните файлове (WhiteNoise ще ги обслужва)
# Подаваме фиктивен SECRET_KEY, за да премине проверката без реален .env файл при build
RUN SECRET_KEY=build-time-key DATABASE_URL=postgres://user:pass@localhost:5432/db python manage.py collectstatic --noinput

# 8. Отваряне на порт 8000 за външен трафик
EXPOSE 8000

# 9. Стартиране на приложението с Gunicorn (WSGI сървър за продукция)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ColourmanBoard.wsgi:application"]

