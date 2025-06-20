FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copia el archivo de requerimientos específico de este servicio
COPY ./backend_model/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código y los datos de este servicio
COPY ./common /app/common
COPY ./backend_model /app/backend_model
COPY ./data /app/data

EXPOSE 8001

# Ejecuta el objeto 'app' desde 'main.py' dentro del paquete 'backend_model'
CMD ["uvicorn", "backend_model.main:app", "--host", "0.0.0.0", "--port", "8001"]