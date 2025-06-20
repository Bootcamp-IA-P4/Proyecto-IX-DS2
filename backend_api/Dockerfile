FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copia el archivo de requerimientos específico de este servicio
COPY ./backend_api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código específico de este servicio
COPY ./common /app/common
COPY ./backend_api /app/backend_api

EXPOSE 8000

# Ejecuta el objeto 'app' desde 'main.py' dentro del paquete 'backend_api'
CMD ["uvicorn", "backend_api.main:app", "--host", "0.0.0.0", "--port", "8000"]