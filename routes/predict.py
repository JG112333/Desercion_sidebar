import base64
import boto3
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  
import io
from flask import Blueprint, request, render_template
from models.model import model
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_S3_BUCKET
from utils.decorators import login_required

# Configurar el cliente de S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,  
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,  
    region_name=AWS_REGION  
)

BUCKET_NAME = AWS_S3_BUCKET

predict_bp = Blueprint('predict', __name__)




@predict_bp.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        # Recoger datos del formulario HTML
        nombre_completo = request.form['nombre_completo'] 
        estado_civil = int(request.form['estado_civil'])
        modo_admision = int(request.form['modo_admision'])
        asistencia = int(request.form['asistencia'])
        cualificacion_previa = int(request.form['cualificacion_previa'])
        ocupacion_madre = int(request.form['ocupacion_madre'])
        ocupacion_padre = int(request.form['ocupacion_padre'])
        desplazado = int(request.form['desplazado'])
        deudor = int(request.form['deudor'])
        cuotas_matricula = int(request.form['cuotas_matricula'])
        genero = int(request.form['genero'])
        becado = int(request.form['becado'])
        edad_inscripcion = int(request.form['edad_inscripcion'])
        materias_1er_sem_acreditadas = int(request.form['materias_1er_sem_acreditadas'])
        materias_1er_sem_matriculadas = int(request.form['materias_1er_sem_matriculadas'])
        materias_1er_sem_evaluaciones = int(request.form['materias_1er_sem_evaluaciones'])
        materias_1er_sem_aprobadas = int(request.form['materias_1er_sem_aprobadas'])
        materias_1er_sem_calificacion = float(request.form['materias_1er_sem_calificacion'])
        materias_1er_sem_sin_evaluaciones = int(request.form['materias_1er_sem_sin_evaluaciones'])
        materias_2do_sem_acreditadas = int(request.form['materias_2do_sem_acreditadas'])
        materias_2do_sem_matriculadas = int(request.form['materias_2do_sem_matriculadas'])
        materias_2do_sem_evaluaciones = int(request.form['materias_2do_sem_evaluaciones'])
        materias_2do_sem_aprobadas = int(request.form['materias_2do_sem_aprobadas'])
        materias_2do_sem_calificacion = float(request.form['materias_2do_sem_calificacion'])
        materias_2do_sem_sin_evaluaciones = int(request.form['materias_2do_sem_sin_evaluaciones'])
        pib = float(request.form['pib'])
 
        # Crear un diccionario con los datos
        datos_json = {
            "nombre_completo": nombre_completo,
            "estado_civil": estado_civil,
            "modo_admision": modo_admision,
            "asistencia": asistencia,
            "cualificacion_previa": cualificacion_previa,
            "ocupacion_madre": ocupacion_madre,
            "ocupacion_padre": ocupacion_padre,
            "desplazado": desplazado,
            "deudor": deudor,
            "cuotas_matricula": cuotas_matricula,
            "genero": genero,
            "becado": becado,
            "edad_inscripcion": edad_inscripcion,
            "materias_1er_sem_acreditadas": materias_1er_sem_acreditadas,
            "materias_1er_sem_matriculadas": materias_1er_sem_matriculadas,
            "materias_1er_sem_evaluaciones": materias_1er_sem_evaluaciones,
            "materias_1er_sem_aprobadas": materias_1er_sem_aprobadas,
            "materias_1er_sem_calificacion": materias_1er_sem_calificacion,
            "materias_1er_sem_sin_evaluaciones": materias_1er_sem_sin_evaluaciones,
            "materias_2do_sem_acreditadas": materias_2do_sem_acreditadas,
            "materias_2do_sem_matriculadas": materias_2do_sem_matriculadas,
            "materias_2do_sem_evaluaciones": materias_2do_sem_evaluaciones,
            "materias_2do_sem_aprobadas": materias_2do_sem_aprobadas,
            "materias_2do_sem_calificacion": materias_2do_sem_calificacion,
            "materias_2do_sem_sin_evaluaciones": materias_2do_sem_sin_evaluaciones,
            "pib": pib,
            "timestamp": datetime.utcnow().isoformat()  # Agregar timestamp
        }

        # Convertir a JSON
        datos_json_str = json.dumps(datos_json)

        # Definir el nombre del archivo en S3
        file_name = f"archivosJSON_s3/{nombre_completo.replace(' ', '_')}_{int(datetime.utcnow().timestamp())}.json"

        # Subir archivo a S3
        s3_client.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=datos_json_str, ContentType='application/json')


        # Crear un DataFrame con los datos de entrada
        input_data = pd.DataFrame([[estado_civil, modo_admision, asistencia, cualificacion_previa, 
                                     ocupacion_madre, ocupacion_padre, desplazado, deudor, cuotas_matricula,
                                     genero, becado, edad_inscripcion, materias_1er_sem_acreditadas, 
                                     materias_1er_sem_matriculadas, materias_1er_sem_evaluaciones, 
                                     materias_1er_sem_aprobadas, materias_1er_sem_calificacion  * 2, 
                                     materias_1er_sem_sin_evaluaciones, materias_2do_sem_acreditadas, 
                                     materias_2do_sem_matriculadas, materias_2do_sem_evaluaciones, 
                                     materias_2do_sem_aprobadas, materias_2do_sem_calificacion * 2, 
                                     materias_2do_sem_sin_evaluaciones, pib]],
                                   columns=['Estado civil', 'Modo de admision', 'Asistencia diurna o nocturna', 'Cualificacion previa', 
                                            'Ocupacion de la madre', 'Ocupacion del padre', 'Desplazado', 'Deudor', 'Cuotas de matricula al dia',
                                            'Genero', 'Becado', 'Edad al inscribirse', 'Materias 1er sem (acreditadas)', 
                                            'Materias 1er sem (matriculadas)', 'Materias 1er sem (evaluaciones)', 
                                            'Materias 1er sem (aprobadas)', 'Materias 1er sem (calificacion)', 
                                            'Materias 1er sem (sin evaluaciones)', 'Materias 2do sem (acreditadas)', 
                                            'Materias 2do sem (matriculadas)', 'Materias 2do sem (evaluaciones)', 
                                            'Materias 2do sem (aprobadas)', 'Materias 2do sem (calificacion)', 
                                            'Materias 2do sem (sin evaluaciones)', 'PIB'])
 
        # Hacer la predicción
        prediction = model.predict(input_data)
        probabilidad = model.predict_proba(input_data)[:, 1]
        probabilidad_desercion = 1 - probabilidad
 
        # Generar el gráfico con Matplotlib
        labels = ['No deserción', 'Deserción']
        values = [probabilidad[0], probabilidad_desercion[0]]
 
        plt.figure(figsize=(6, 4))
        plt.bar(labels, values, color=['green', 'red'])
        plt.title("Gráfico de probabilidades")
        plt.xlabel('Estado')
        plt.ylabel('Probabilidad')
 
        # Guardar la imagen en memoria usando BytesIO
        img_io = io.BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)  # Volver al inicio del archivo en memoria
        plt.close()  # Cerrar la figura de Matplotlib para liberar recursos
 
        # Convertir la imagen a base64
        img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
 
        # Renderizar la plantilla con los datos
        return render_template('resultados.html', 
                               resultado="No desertará" if prediction[0] == 1 else "Desertará",
                               probabilidad=probabilidad[0],
                               probabilidad_desercion=probabilidad_desercion[0],
                               chart_img=img_base64)
    except Exception as e:
        return f"Error: {e}"