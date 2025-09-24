# Imagen base ligera de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias de sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements si los tienes (opcional)
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Instalar Flask y Gunicorn directamente
RUN pip install --no-cache-dir flask gunicorn flask-cors

# Copiar el código de la app
COPY main.py /app

# Exponer el puerto
EXPOSE 5000

# Comando de arranque con Gunicorn
# "app:app" → nombre_archivo:objeto_flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "main:app"]
