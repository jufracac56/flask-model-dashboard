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
    # Esta ruta recibe datos JSON a través de una solicitud POST para realizar una predicción.
    data = request.json  # Obtiene los datos JSON enviados en la solicitud.
    
    # Prepara las características (features) que el modelo necesita para hacer una predicción.
    features = [[
        data['sepal_length'],
        data['sepal_width'],
        data['petal_length'],
        data['petal_width']
    ]]
    
    # Realiza la predicción usando el modelo previamente cargado.
    prediction = model.predict(features)[0]  # Predicción basada en las características.

    # Guarda la predicción en la base de datos para poder consultarla más tarde.
    new_prediction = Prediction(
        sepal_length=data['sepal_length'],
        sepal_width=data['sepal_width'],
        petal_length=data['petal_length'],
        petal_width=data['petal_width'],
        predicted_class=prediction  # Guarda la clase predicha en la base de datos.
    )
    db.session.add(new_prediction)  # Agrega la predicción a la sesión de la base de datos.
    db.session.commit()  # Confirma los cambios en la base de datos.

    # Retorna la predicción como respuesta JSON.
    return jsonify({'prediction': prediction})

# Ruta para obtener todas las predicciones realizadas (GET).
@app.route('/predictions', methods=['GET'])
def get_predictions():
    # Esta ruta obtiene todas las predicciones almacenadas en la base de datos.
    predictions = Prediction.query.all()  # Obtiene todas las predicciones de la base de datos.
    
    # Prepara los datos de las predicciones para ser retornados como JSON.
    result = [{'id': pred.id, 'sepal_length': pred.sepal_length, 'sepal_width': pred.sepal_width,
               'petal_length': pred.petal_length, 'petal_width': pred.petal_width, 'predicted_class': pred.predicted_class}
              for pred in predictions]  # Convierte las predicciones a un formato de lista de diccionarios.

    return jsonify(result)  # Retorna las predicciones en formato JSON.

# Ruta para actualizar una predicción existente (PUT).
@app.route('/prediction/<int:id>', methods=['PUT'])
def update_prediction(id):
    # Esta ruta actualiza una predicción existente en la base de datos.
    data = request.json  # Obtiene los datos JSON enviados en la solicitud.
    
    # Busca la predicción en la base de datos usando el ID proporcionado en la URL.
    prediction = Prediction.query.get(id)  # Busca la predicción por su ID.
    
    if not prediction:
        # Si no se encuentra la predicción, devuelve un mensaje de error.
        return jsonify({'message': 'Prediction not found'}), 404

    # Actualiza los campos de la predicción con los nuevos valores proporcionados (si existen).
    prediction.sepal_length = data.get('sepal_length', prediction.sepal_length)
    prediction.sepal_width = data.get('sepal_width', prediction.sepal_width)
    prediction.petal_length = data.get('petal_length', prediction.petal_length)
    prediction.petal_width = data.get('petal_width', prediction.petal_width)

    # Realiza la predicción nuevamente con las características actualizadas.
    features = [[
        prediction.sepal_length,
        prediction.sepal_width,
        prediction.petal_length,
        prediction.petal_width
    ]]
    prediction.predicted_class = model.predict(features)[0]  # Actualiza la clase predicha.

    # Guarda los cambios en la base de datos.
    db.session.commit()  # Confirma los cambios en la base de datos.

    return jsonify({'message': 'Prediction updated'})  # Responde con un mensaje indicando que la predicción fue actualizada.

# Ruta para actualizar parcialmente una predicción existente (PATCH).
@app.route('/prediction/<int:id>', methods=['PATCH'])
def patch_prediction(id):
    # Esta ruta permite actualizar parcialmente una predicción existente.
    data = request.json  # Obtiene los datos JSON enviados en la solicitud.
    
    # Busca la predicción en la base de datos usando el ID proporcionado en la URL.
    prediction = Prediction.query.get(id)
    
    if not prediction:
        # Si no se encuentra la predicción, devuelve un mensaje de error.
        return jsonify({'message': 'Prediction not found'}), 404

    # Solo actualiza los campos que están presentes en los datos enviados.
    if 'sepal_length' in data:
        prediction.sepal_length = data['sepal_length']
    if 'sepal_width' in data:
        prediction.sepal_width = data['sepal_width']
    if 'petal_length' in data:
        prediction.petal_length = data['petal_length']
    if 'petal_width' in data:
        prediction.petal_width = data['petal_width']

    # Realiza la predicción nuevamente con las características actualizadas.
    features = [[
        prediction.sepal_length,
        prediction.sepal_width,
        prediction.petal_length,
        prediction.petal_width
    ]]
    prediction.predicted_class = model.predict(features)[0]  # Actualiza la clase predicha.

    # Guarda los cambios en la base de datos.
    db.session.commit()

    return jsonify({'message': 'Prediction partially updated'})  # Responde con un mensaje indicando que la predicción fue parcialmente actualizada.

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




# @app.route('/metrics', methods=['GET'])
# def get_metrics():
#     try:
#         # Intenta leer las métricas desde un archivo JSON.
#         with open('metrics.json', 'r') as f:
#             metrics = json.load(f)  # Carga el archivo JSON que contiene las métricas.

#         # Asume que el archivo JSON tiene las métricas necesarias como 'accuracy', 'f1_score', 'precision', 'recall'.
#         labels = ['Accuracy', 'F1 Score', 'Precision', 'Recall']  # Etiquetas para el gráfico.
#         data = [
#             metrics['accuracy'],
#             metrics['f1_score'],
#             metrics['precision'],
#             metrics['recall']
#         ]  # Los valores de las métricas.

#         return jsonify({'labels': labels, 'data': data}), 200  # Retorna las métricas en formato JSON.

#     except FileNotFoundError:
#         # Si el archivo metrics.json no se encuentra, retorna un error.
#         return jsonify({'error': 'Metrics file not found'}), 404

# Ruta para mostrar el dashboard con las métricas.
@app.route('/dashboard')
def dashboard():
    try:
        # Aquí puedes llamar a la ruta /metrics para obtener las métricas directamente.
        metrics = {
            "labels": ["Accuracy", "Precision", "Recall", "F1 Score"],
            "data": [0.9, 0.921, 0.9, 0.896]
        }
        # Retorna la plantilla HTML (dashboard.html) y pasa las métricas como contexto.
        return render_template('dashboard.html', metrics=metrics)
    
    except Exception as e:
        # Si ocurre algún error al cargar el dashboard, responde con un mensaje de error.
        return jsonify({'error': 'Error al cargar el dashboard', 'message': str(e)}), 500

# Ejecutar la aplicación Flask.
if __name__ == '__main__':
    # Ejecutar la aplicación en el host '0.0.0.0' (para aceptar conexiones externas) y el puerto 5000.
    app.run(host='0.0.0.0', port=5000)
