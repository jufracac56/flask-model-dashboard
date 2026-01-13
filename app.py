#app.py
#Importación de librerias
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pickle
import json

# Inicialización de la aplicación Flask y la base de datos.
app = Flask(__name__)  # Crea una instancia de la aplicación Flask.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'  # Configura la base de datos SQLite para almacenar las predicciones.
db = SQLAlchemy(app)  # Se inicializa la instancia de la base de datos.

# Cargar el modelo entrenado desde un archivo usando pickle.
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)  # Deserializa el archivo .pkl que contiene el modelo entrenado.

# Definir el modelo de la base de datos que representa las predicciones.
class Prediction(db.Model):
    # Define una tabla de la base de datos llamada "Prediction" para almacenar predicciones.
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada predicción.
    sepal_length = db.Column(db.Float, nullable=False)  # Longitud del sépalo.
    sepal_width = db.Column(db.Float, nullable=False)  # Ancho del sépalo.
    petal_length = db.Column(db.Float, nullable=False)  # Longitud del pétalo.
    petal_width = db.Column(db.Float, nullable=False)  # Ancho del pétalo.
    predicted_class = db.Column(db.String, nullable=True)  # Clase predicha (como string, por ejemplo, 'Setosa').

# Crear las tablas de la base de datos si no existen aún.
with app.app_context():
    db.create_all()  # Crea las tablas en la base de datos si no existen.

# Ruta para realizar predicciones (POST).
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Validación de campos obligatorios
    required_fields = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    # Validación de tipos numéricos
    try:
        features = [[
            float(data['sepal_length']),
            float(data['sepal_width']),
            float(data['petal_length']),
            float(data['petal_width'])
        ]]
    except ValueError:
        return jsonify({'error': 'All fields must be numeric'}), 400

    prediction = model.predict(features)[0]

    new_prediction = Prediction(
        sepal_length=data['sepal_length'],
        sepal_width=data['sepal_width'],
        petal_length=data['petal_length'],
        petal_width=data['petal_width'],
        predicted_class=prediction
    )
    db.session.add(new_prediction)
    db.session.commit()
    return jsonify({'prediction': prediction})

# Ruta para obtener todas las predicciones realizadas (GET).
@app.route('/predictions', methods=['GET'])
def get_predictions():
    # Límite por parámetro GET
    limit = request.args.get('limit', default=10, type=int)
    MAX_LIMIT = 100
    if limit > MAX_LIMIT:
        limit = MAX_LIMIT
    query = Prediction.query
    predictions = query.limit(limit).all()
    result = [{
        'id': pred.id,
        'sepal_length': pred.sepal_length,
        'sepal_width': pred.sepal_width,
        'petal_length': pred.petal_length,
        'petal_width': pred.petal_width,
        'predicted_class': pred.predicted_class
    } for pred in predictions]
    return jsonify({
        'count': len(result),
        'limit': limit,
        'data': result
    })

# Ruta para actualizar una predicción existente (PUT).
@app.route('/prediction/<int:id>', methods=['PUT'])
def update_prediction(id):
    data = request.json
    required_fields = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
        if not isinstance(data[field], (float, int)):
            return jsonify({'error': f'Invalid type for {field}: must be a number'}), 400
    prediction = Prediction.query.get(id)
    if not prediction:
        return jsonify({'message': 'Prediction not found'}), 404
    prediction.sepal_length = data.get('sepal_length', prediction.sepal_length)
    prediction.sepal_width = data.get('sepal_width', prediction.sepal_width)
    prediction.petal_length = data.get('petal_length', prediction.petal_length)
    prediction.petal_width = data.get('petal_width', prediction.petal_width)
    features = [[
        prediction.sepal_length,
        prediction.sepal_width,
        prediction.petal_length,
        prediction.petal_width
    ]]
    prediction.predicted_class = model.predict(features)[0]
    db.session.commit()
    return jsonify({'message': 'Prediction updated'})

# Ruta para actualizar parcialmente una predicción existente (PATCH).
@app.route('/prediction/<int:id>', methods=['PATCH'])
def patch_prediction(id):
    data = request.json
    if not data:
        return jsonify({'error': 'No fields provided for update'}), 400
    valid_fields = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    for key, value in data.items():
        if key in valid_fields:
            if not isinstance(value, (int, float)):
                return jsonify({'error': f'Invalid type for {key}: must be a number'}), 400
    prediction = Prediction.query.get(id)
    if not prediction:
        return jsonify({'message': 'Prediction not found'}), 404
    if 'sepal_length' in data:
        prediction.sepal_length = data['sepal_length']
    if 'sepal_width' in data:
        prediction.sepal_width = data['sepal_width']
    if 'petal_length' in data:
        prediction.petal_length = data['petal_length']
    if 'petal_width' in data:
        prediction.petal_width = data['petal_width']
    features = [[
        prediction.sepal_length,
        prediction.sepal_width,
        prediction.petal_length,
        prediction.petal_width
    ]]
    prediction.predicted_class = model.predict(features)[0]
    db.session.commit()
    return jsonify({'message': 'Prediction partially updated'})

# Ruta para obtener las métricas del modelo (GET).
@app.route('/metrics', methods=['GET'])
def get_metrics():
    try:
        # Leer las métricas completas desde el archivo JSON
        with open('metrics.json', 'r') as f:
            metrics = json.load(f)  # Carga todo el archivo JSON

        # Devolver toda la estructura completa que contiene:
        # - accuracy, precision, recall, f1_score
        # - confusion_matrix
        # - classification_report
        return jsonify(metrics), 200

    except FileNotFoundError:
        # Si el archivo metrics.json no se encuentra, retorna un error
        return jsonify({'error': 'Metrics file not found'}), 404
    except json.JSONDecodeError:
        # Si hay un error al decodificar el JSON
        return jsonify({'error': 'Invalid JSON format in metrics file'}), 400
    except Exception as e:
        # Cualquier otro error
        return jsonify({'error': 'Error loading metrics', 'message': str(e)}), 500

# Ruta para mostrar el dashboard con las métricas.
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Ejecutar la aplicación Flask.
if __name__ == '__main__':
    # Ejecutar la aplicación en el host '0.0.0.0' (para aceptar conexiones externas) y el puerto 5000.
    app.run(host='0.0.0.0', port=5000)
