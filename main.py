from flask import Flask, request, jsonify
from flask_cors import CORS

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
    # Devolver un JSON simple en la raíz
    return jsonify(message="API de mascotas. Use /mascotas para obtener la lista")


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