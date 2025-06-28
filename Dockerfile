FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONPATH=/app

ENV DJANGO_SETTINGS_MODULE=ultralg.ultralg.settings

CMD ["sh", "-c", "gunicorn ultralg.ultralg.wsgi:application --bind 0.0.0.0:8000 --workers $((2 * $(nproc) + 1))"]
