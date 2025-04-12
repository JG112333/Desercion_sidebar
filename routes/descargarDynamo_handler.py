from flask import Blueprint, redirect, render_template, request, send_file, url_for
import pandas as pd
import os
import boto3  # Importar boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import utils.diccionario_handler as dh
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION2, AWS_DYNAMODB_TABLE
from utils.decorators import admin_required

# Conectar a DynamoDB con credenciales explícitas
DYNAMO_TABLE = AWS_DYNAMODB_TABLE

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,  
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
    region_name=AWS_REGION2
)
table = dynamodb.Table(DYNAMO_TABLE)

descargarDynamo_bp = Blueprint('descargarDynamo_handler', __name__)

# Orden y nombres deseados de las columnas
COLUMN_ORDER = [
    "nombre_completo", "estado_civil", "modo_admision", "asistencia", "cualificacion_previa",
    "ocupacion_madre", "ocupacion_padre", "desplazado", "deudor", "cuotas_matricula", "genero", 
    "becado", "edad_inscripcion", "materias_1er_sem_acreditadas", "materias_1er_sem_matriculadas", 
    "materias_1er_sem_evaluaciones", "materias_1er_sem_aprobadas", "materias_1er_sem_calificacion", 
    "materias_1er_sem_sin_evaluaciones", "materias_2do_sem_acreditadas", "materias_2do_sem_matriculadas", 
    "materias_2do_sem_evaluaciones", "materias_2do_sem_aprobadas", "materias_2do_sem_calificacion", 
    "materias_2do_sem_sin_evaluaciones", "pib", "timestamp"
]


@descargarDynamo_bp.route('/procesar_Reporte',  methods=['GET', 'POST'])
@admin_required
def procesar_Reporte():
    """ Procesar desde DynamoDB"""
    # if request.method == 'GET':
    #     return redirect(url_for('home.home'))  # Redirige a la vista 'home' del blueprint 'home'
    
    try:
        # Obtener datos de DynamoDB
        response = table.scan()
        items = response.get('Items', [])
        
        if not items:
            return render_template('descargarDynamo.html', mensaje_error="Error: No hay datos en DynamoDB")
        
        # Convertir a DataFrame
        df = pd.DataFrame(items)

        # Reordenar las columnas según el orden deseado
        df = df[COLUMN_ORDER]
        
        # Renombrar columnas para que coincidan con los nombres deseados
        column_mapping = {
             "nombre_completo": "Nombre completo",
             "estado_civil": "Estado civil",
             "modo_admision": "Modo de admision",
             "asistencia": "Asistencia diurna o nocturna",
             "cualificacion_previa": "Cualificacion previa",
             "ocupacion_madre": "Ocupacion de la madre",
             "ocupacion_padre": "Ocupacion del padre",
             "desplazado": "Desplazado",
             "deudor": "Deudor",
             "cuotas_matricula": "Cuotas de matricula al dia",
             "genero": "Genero",
             "becado": "Becado",
             "edad_inscripcion": "Edad al inscribirse",
             "materias_1er_sem_acreditadas": "Materias 1er sem (acreditadas)",
             "materias_1er_sem_matriculadas": "Materias 1er sem (matriculadas)",
             "materias_1er_sem_evaluaciones": "Materias 1er sem (evaluaciones)",
             "materias_1er_sem_aprobadas": "Materias 1er sem (aprobadas)",
             "materias_1er_sem_calificacion": "Materias 1er sem (calificacion)",
             "materias_1er_sem_sin_evaluaciones": "Materias 1er sem (sin evaluaciones)",
             "materias_2do_sem_acreditadas": "Materias 2do sem (acreditadas)",
             "materias_2do_sem_matriculadas": "Materias 2do sem (matriculadas)",
             "materias_2do_sem_evaluaciones": "Materias 2do sem (evaluaciones)",
             "materias_2do_sem_aprobadas": "Materias 2do sem (aprobadas)",
             "materias_2do_sem_calificacion": "Materias 2do sem (calificacion)",
             "materias_2do_sem_sin_evaluaciones": "Materias 2do sem (sin evaluaciones)",
             "pib": "PIB",
             "timestamp": "Fecha"
         }
        df.rename(columns=column_mapping, inplace=True)

        # Asegurar que la columna Fecha sea de tipo datetime
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        # Ordenar por Fecha en orden ascendente (de más antiguo a más reciente)
        df = df.sort_values(by='Fecha', ascending=True)

        # Convertir números a texto
        df['Estado civil'] = df['Estado civil'].map(dh.estado_civil_inv)
        df['Modo de admision'] = df['Modo de admision'].map(dh.modo_admision_inv)
        df['Asistencia diurna o nocturna'] = df['Asistencia diurna o nocturna'].map(dh.asistencia_inv)
        df['Cualificacion previa'] = df['Cualificacion previa'].map(dh.cualificacion_previa_inv)
        df['Ocupacion de la madre'] = df['Ocupacion de la madre'].map(dh.ocupacion_madre_inv)
        df['Ocupacion del padre'] = df['Ocupacion del padre'].map(dh.ocupacion_padre_inv)
        df['Desplazado'] = df['Desplazado'].map(dh.desplazado_inv)
        df['Deudor'] = df['Deudor'].map(dh.deudor_inv)
        df['Cuotas de matricula al dia'] = df['Cuotas de matricula al dia'].map(dh.matricula_al_dia_inv)
        df['Genero'] = df['Genero'].map(dh.genero_inv)
        df['Becado'] = df['Becado'].map(dh.becado_inv)
        
        # Guardar el archivo XLSX
        output_path = 'static/Reporte.xlsx'
        df.to_excel(output_path, index=False)
        
        return render_template('descargarDynamo.html', archivo_generado=True)
    
    except (NoCredentialsError, PartialCredentialsError):
        return render_template('descargarDynamo.html', mensaje_error="Error: Credenciales de AWS no configuradas correctamente")
    except Exception as e:
        print(f"Error general: {str(e)}")
        return render_template('descargarDynamo.html', mensaje_error=f"Error procesando datos de DynamoDB: {str(e)}")

@descargarDynamo_bp.route('/descargar_Reporte')
@admin_required
def descargar_Reporte():
    """ Descarga el XLSX generado """
    output_path = 'static/Reporte.xlsx'
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return "No hay archivo disponible para descargar", 404
