El modelo a generar deberá contar con la estructura: 

flask_model_dashboard/

│

├── app.py                 # El archivo principal de la aplicación Flask.

├── model.pkl              # El modelo entrenado que se carga en Flask.

├── metrics.json           # El archivo donde se guardan las métricas del modelo.

├── templates/

│   ├── dashboard.html     # El archivo HTML para mostrar el dashboard con Chart.js.

├── requirements.txt       # Dependencias necesarias para ejecutar el proyecto.

└── README.md              # Instrucciones y descripción del proyecto.



Nota: Al final de las instrucciones encontrará los archivos necesarios para la actividad.



Cree el directorio proyectoDashboard en la instancia de cloud9

Ingrese al directorio proyectoDashboard

Suba los archivos api.py, iris.csv, model.py, requirements.txt

Cree el directorio templates

Dentro del directorio templates suba el archivo dashboard.html 



Cree el ambiente virtual: 

python -m venv dashboard

Active el entorno:

source dashboard/bin/activate



Dentro del entorno virtual instale los requerimientos:

pip install -r requirements.txt



Después de instalar requirements.txt, es necesario actualizar:

pip install --upgrade Flask-SQLAlchemy



Ejecute el entrenamiento del modelo con:

python model.py



Ejecute la instancia para comunicación del modelo a través de Flask:

python app.py



En una terminal escriba lo indicado para cada método

1. Método POST: Hacer una nueva predicción

curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{

    "sepal_length": 5.1,

    "sepal_width": 3.5,

    "petal_length": 1.4,

    "petal_width": 0.2

}'



2. Método GET: Obtener todas las predicciones

curl http://127.0.0.1:5000/predictions



3. Método PUT: Actualizar una predicción existente

curl -X PUT http://127.0.0.1:5000/prediction/1 -H "Content-Type: application/json" -d '{

    "sepal_length": 5.7,

    "sepal_width": 3.2,

    "petal_length": 1.5,

    "petal_width": 0.3

}'



4. Método PATCH: Actualizar parcialmente una predicción

curl -X PATCH http://127.0.0.1:5000/prediction/1 -H "Content-Type: application/json" -d '{

    "sepal_length": 5.8

}'



5.- Consulta de métricas: accuracy, confusion_matrix, f1_score, precision y recall 

curl http://127.0.0.1:5000/metrics



Instale Postman, lo puede descargar en: https://www.postman.com/downloads/



Configurar la EC2 que corresponde a su servicios de CLOUD9 (Su ya tiene salida a internet, no es necesaria la configuración)

Ahora debe ingresar a EC2.

Dé clic en el id de su instancia

Dé clic en la pestaña inferior "Seguridad"

Dé clic en "Grupos de seguridad"

Dé clic en "Id del grupo de seguridad"

Dé clic en "Editar reglas de entrada"

Dé clci en "Agregar regla"

Tipo: TCP Personalizado

Protocolo: TCP

Intervalo de puertos: 5000

Origen: Personalizada

Blokes de CIDR: 0.0.0.0/0

Descripción: Acceso Flask



Copie su dirección ip pública, la utilizará en adelante:



Ahora debe ejecutar

1. Método POST: Hacer una nueva predicción

Abrir Postman.



Selecciona el método POST en el menú desplegable.

Ingresa la URL: http://escribasuippublica:5000/predict.

Ve a la pestaña Headers:

Agrega una clave: Content-Type con el valor application/json.

Ve a la pestaña Body:

Selecciona raw y escribe el cuerpo en formato JSON:

json

{

    "sepal_length": 5.1,

    "sepal_width": 3.5,

    "petal_length": 1.4,

    "petal_width": 0.2

}

Haga clic en Send.

Si todo está correcto, deberías recibir una respuesta con el detalle de la predicción.



2. Método GET: Obtener todas las predicciones

Selecciona el método GET en el menú desplegable.

Ingresa la URL: http://54.90.64.177:5000/predictions.

Haz clic en Send.



Debería recibir un JSON con la lista de todas las predicciones realizadas.



3. Método PUT: Actualizar una predicción existente

Selecciona el método PUT.



Ingrese la URL: http://54.90.64.177:5000/prediction/1 (reemplaza 1 con el ID de la predicción que deseas actualizar).



Vaya a la pestaña Headers:

Agregue Content-Type con el valor application/json.

Ve a la pestaña Body:

Selecciona raw y escribe el cuerpo en JSON:

{

    "sepal_length": 5.7,

    "sepal_width": 3.2,

    "petal_length": 1.5,

    "petal_width": 0.3

}

Haga clic en Send.



Debería recibir la predicción actualizada.



5. Consulta de métricas

Selecciona el método GET.

Ingrese la URL: http://54.90.64.177:5000/metrics.

Haga clic en Send.

Debería recibir un JSON con las métricas, como accuracy, confusion_matrix, f1_score, etc.



Genere un reporte con imágenes de los pasos descritos anteriormente.



Consulte el dashboard con las métricas:

Para ello abra un navegador:

http://suippublica:5000/dashboard



Por último modifique el dashboard para cambiar el tipo de gráfico o incluir una métrica adicional, genere un vídeo adicional en el que se evidencie cada paso y súbalo a la plataforma (En caso de ser necesario puede compartir el enlace al vídeo).

