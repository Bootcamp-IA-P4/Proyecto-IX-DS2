# Usa una versión estable y segura
FROM python:3.12-slim

# (Opcional pero recomendado) Paso de actualización de seguridad
RUN apt-get update && apt-get upgrade -y --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los requerimientos y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto (todo, ya que el contexto es la raíz)
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# --- ¡LA LÍNEA CLAVE! ---
# Cambiamos el comando para que sea igual al que funciona en local,
# especificando la ruta completa del módulo desde el Workdir (/app).
# Uvicorn ahora sabrá que está corriendo un módulo dentro de un paquete.
CMD ["uvicorn", "fast_api.main:app", "--host", "0.0.0.0", "--port", "8000"]