# Importación de librerías necesarias
import pandas as pd
from sklearn.model_selection import train_test_split  # Para dividir el conjunto de datos en entrenamiento y prueba
from sklearn.linear_model import LogisticRegression  # Para el modelo de regresión logística
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report  # Métricas de evaluación
import pickle  # Para guardar y cargar el modelo entrenado
import json  # Para guardar las métricas en formato JSON

def load_data(file_path):
    """
    Carga el dataset desde un archivo CSV.
    
    Parámetros:
    - file_path: Ruta al archivo CSV que contiene los datos.
    
    Retorna:
    - Un DataFrame de Pandas con los datos cargados.
    
    Si el archivo no se encuentra, se lanza un error FileNotFoundError.
    """
    try:
        # Intentamos cargar el dataset desde el archivo CSV especificado.
        data = pd.read_csv(file_path)
        print(f"Dataset cargado con éxito desde {file_path}.")  # Mensaje de éxito
        return data
    except FileNotFoundError:
        # En caso de que no se encuentre el archivo, se lanza un error y se imprime un mensaje.
        print(f"Error: No se encontró el archivo {file_path}.")
        raise  # Lanza el error hacia arriba para que el flujo se detenga.

def train_and_evaluate_model(X_train, X_test, y_train, y_test):
    """
    Entrena un modelo de regresión logística y evalúa su rendimiento utilizando las métricas adecuadas.
    
    Parámetros:
    - X_train: Datos de entrada para el entrenamiento.
    - X_test: Datos de entrada para las pruebas.
    - y_train: Etiquetas de salida para el entrenamiento.
    - y_test: Etiquetas de salida para las pruebas.
    
    Retorna:
    - model: El modelo entrenado.
    - metrics: Un diccionario con las métricas de evaluación.
    """
    # Crear un modelo de regresión logística.
    model = LogisticRegression(max_iter=200)  # Definimos el modelo con un número máximo de iteraciones de 200.
    
    # Entrenamos el modelo usando los datos de entrenamiento.
    model.fit(X_train, y_train)
    
    # Realizamos las predicciones con el modelo entrenado utilizando el conjunto de prueba.
    y_pred = model.predict(X_test)
    
    #Agregamos una metrica
    class_report = classification_report(y_test, y_pred, output_dict=True)
    
    # Calculamos las métricas de evaluación del modelo.
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),  # Exactitud del modelo.
        'precision': precision_score(y_test, y_pred, average='weighted'),  # Precisión ponderada.
        'recall': recall_score(y_test, y_pred, average='weighted'),  # Sensibilidad ponderada.
        'f1_score': f1_score(y_test, y_pred, average='weighted'),  # Puntuación F1 ponderada.
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),# Matriz de confusión.
        'classification_report': class_report
    }
    
    # Retornamos el modelo entrenado y el diccionario de métricas.
    return model, metrics

def save_model_and_metrics(model, metrics, model_path='model.pkl', metrics_path='metrics.json'):
    """
    Guarda el modelo y las métricas en archivos específicos.
    
    Parámetros:
    - model: El modelo entrenado.
    - metrics: Un diccionario con las métricas de evaluación.
    - model_path: Ruta para guardar el modelo entrenado (por defecto 'model.pkl').
    - metrics_path: Ruta para guardar las métricas en formato JSON (por defecto 'metrics.json').
    """
    # Guardamos el modelo entrenado utilizando pickle.
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Modelo guardado en {model_path}.")  # Mensaje de éxito al guardar el modelo.
    
    # Guardamos las métricas en formato JSON.
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"Métricas guardadas en {metrics_path}.")  # Mensaje de éxito al guardar las métricas.

def train_model():
    """
    Función principal para entrenar el modelo y guardar tanto el modelo como las métricas.
    
    Esta función carga los datos, entrena el modelo, evalúa el rendimiento y guarda los resultados.
    """
    # Cargamos los datos desde el archivo 'iris.csv'.
    data = load_data('iris.csv')
    
    # Separamos las características (X) y las etiquetas (y) del conjunto de datos.
    X = data.iloc[:, :-1]  # Todas las columnas excepto la última (características).
    y = data.iloc[:, -1]   # Solo la última columna (etiquetas).
    
    # Dividimos los datos en un conjunto de entrenamiento y un conjunto de prueba (80%-20%).
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Entrenamos el modelo y calculamos las métricas de evaluación.
    model, metrics = train_and_evaluate_model(X_train, X_test, y_train, y_test)
    
    # Guardamos el modelo entrenado y las métricas en archivos.
    save_model_and_metrics(model, metrics)

def load_trained_model(model_path='model.pkl'):
    """
    Carga el modelo entrenado desde un archivo.
    
    Parámetros:
    - model_path: Ruta del archivo donde se encuentra el modelo guardado (por defecto 'model.pkl').
    
    Retorna:
    - El modelo cargado.
    """
    with open(model_path, 'rb') as f:
        # Cargamos el modelo utilizando pickle.
        model = pickle.load(f)
    return model

def make_prediction(model, features):
    """
    Realiza una predicción con el modelo cargado.
    
    Parámetros:
    - model: El modelo previamente entrenado.
    - features: Un conjunto de características para realizar la predicción.
    
    Retorna:
    - La predicción realizada por el modelo.
    """
    # Realizamos la predicción con el modelo utilizando las características proporcionadas.
    prediction = model.predict([features])
    return prediction[0]  # Retornamos el primer valor de la predicción.

# Si el script se ejecuta directamente, entrenamos el modelo.
if __name__ == '__main__':
    train_model()  # Llamamos a la función que entrena el modelo.
