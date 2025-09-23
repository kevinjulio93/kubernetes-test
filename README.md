# Mascotas - API y Frontend

Este pequeño proyecto contiene una API en Flask y un frontend estático (HTML/CSS/JS) que consume la API para listar, agregar y eliminar mascotas.

Requisitos
- Python 3.9 (ya hay un virtualenv en `env/` en este repo)

Ejecutar backend

1. Activar el virtualenv incluido:

```bash
source env/bin/activate
```

2. Instalar dependencias si faltan (opcional):

```bash
pip install flask flask-cors
```

3. Ejecutar la API:

```bash
python main.py
```

La API escuchará por defecto en http://127.0.0.1:5000

Probar frontend

Puedes servir la carpeta `frontend` con un servidor estático o usar el servidor Node incluido que carga la variable `API_BASE` desde `.env`.

Opción A — servidor Node (recomendado):

```bash
cd frontend
npm install
cp .env.example .env   # editar .env si quieres cambiar la URL
npm start
```

Luego abre http://127.0.0.1:8000 en tu navegador. El servidor expone `/config` para que el frontend lea `API_BASE` desde `.env`.

Opción B — servidor estático mínimo:

```bash
cd frontend
python -m http.server 8000
```

En este caso asegúrate de que `frontend/app.js` apunta a la URL de la API correcta (por defecto `http://127.0.0.1:5000`).

Usar Docker (frontend)

Puedes construir una imagen Docker del frontend y ejecutarla. Desde la carpeta `frontend`:

```bash
# Construir la imagen
docker build -t mascotas-frontend:latest .

# Ejecutar (mapear el puerto y pasar .env si quieres)
docker run -p 8000:8000 --env-file .env mascotas-frontend:latest
```

La app quedará disponible en http://127.0.0.1:8000 y el contenedor leerá `API_BASE` desde el `.env` que pases.

Notas
- El backend almacena las mascotas en memoria; al reiniciar la app se perderán los datos nuevos.
- Si quieres desplegar o persistir datos, añade una base de datos y ajusta los endpoints.
