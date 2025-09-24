# Usar una imagen de node ligera
FROM node:18-alpine

# Crear directorio de la app
WORKDIR /usr/src/app

# Copiar package.json y package-lock.json si existe para instalar deps
COPY package.json package-lock.json* ./

# Instalar dependencias (producción)
RUN npm ci --only=production || npm install --only=production

# Copiar el resto de archivos
COPY . .

# Exponer el puerto (por defecto en .env es 8000)
EXPOSE 8000

# Ejecutar la app
CMD ["node", "server.js"]
