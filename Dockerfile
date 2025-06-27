FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

COPY . .

EXPOSE 8000

CMD ["gunicorn", "ultralg.wsgi:application", "--bind", "0.0.0.0:8000"]
