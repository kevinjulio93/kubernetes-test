from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# Permitir CORS para que el frontend (servido desde otro origen) pueda consumir la API
CORS(app)

# Lista de mascotas de ejemplo (in-memory)
PETS = [
    {"nombre": "Fido", "grupo": "mamífero", "patas": 4, "alimentacion": "carnívoro"},
    {"nombre": "Mittens", "grupo": "mamífero", "patas": 4, "alimentacion": "carnívoro"},
    {"nombre": "Tweety", "grupo": "ave", "patas": 2, "alimentacion": "herbívoro"},
    {"nombre": "Nemo", "grupo": "pez", "patas": 0, "alimentacion": "omnivoro"},
    {"nombre": "Hopper", "grupo": "anfibio", "patas": 4, "alimentacion": "carnívoro"},
    {"nombre": "Bunny", "grupo": "mamífero", "patas": 4, "alimentacion": "herbívoro"},
]


@app.route('/', methods=['GET'])
def greet():
    # Devolver un JSON simple en la raíz, incluyendo variables específicas del entorno si existen
    # Leer sólo desde las variables de entorno del sistema
    env_vars = {
        'APP_SECRET': os.environ.get('APP_SECRET'),
        'API_KEY': os.environ.get('API_KEY'),
        'FRONTEND_TOKEN': os.environ.get('FRONTEND_TOKEN')
    }
    return jsonify(message="API de mascotas. Use /mascotas para obtener la lista", env=env_vars)


@app.route('/mascotas', methods=['GET'])
def get_mascotas():
    return jsonify(mascotas=PETS)


@app.route('/mascotas', methods=['POST'])
def add_mascota():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    grupo = data.get('grupo')
    patas = data.get('patas')
    alimentacion = data.get('alimentacion')

    if not nombre or grupo is None or patas is None or alimentacion is None:
        return jsonify(error='Faltan campos. Se requieren nombre, grupo, patas, alimentacion'), 400

    # Evitar duplicados por nombre
    for p in PETS:
        if p.get('nombre') == nombre:
            return jsonify(error='Mascota con ese nombre ya existe'), 409

    nueva = {"nombre": nombre, "grupo": grupo, "patas": int(patas), "alimentacion": alimentacion}
    PETS.append(nueva)
    return jsonify(mascota=nueva), 201


@app.route('/mascotas/<string:nombre>', methods=['DELETE'])
def delete_mascota(nombre):
    for i, p in enumerate(PETS):
        if p.get('nombre') == nombre:
            PETS.pop(i)
            return jsonify(message='Eliminada'), 200
    return jsonify(error='No encontrada'), 404


if __name__ == '__main__':
    # Ejecutar la app en modo debug en el puerto 5000 por defecto
    app.run(debug=True)


    docker run -d -p 5000:5000 --name k8s-api -e APP_SECRET="$APP_SECRET" -e API_KEY="$API_KEY" -e FRONTEND_TOKEN="$FRONTEND_TOKEN" docker.io/kevinjuliom93/k8s-api:v4