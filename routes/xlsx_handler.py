from flask import Blueprint, request, render_template, send_file
import pandas as pd
import os
import boto3
from models.model import model
from sklearn.exceptions import NotFittedError
import matplotlib.pyplot as plt
import io
import base64
import utils.diccionario_handler as dh
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


xlsx_bp = Blueprint('xlsx_handler', __name__)

@xlsx_bp.route('/procesar_xlsx', methods=['POST'])
@login_required
def procesar_xlsx():
    """ Procesa el archivo XLSX, hace predicciones y genera un gráfico de salida """
    try:
        file = request.files['archivo_xlsx']
        if not file or not file.filename.endswith('.xlsx'):
            return render_template('cargarDatos.html', mensaje_error="Debe ser un archivo XLSX válido")

        df = pd.read_excel(file)  # 📌 Ahora leemos archivos XLSX
        if df.empty:
            return render_template('cargarDatos.html', mensaje_error="El archivo XLSX está vacío")
        
        # Verificar si la columna existe antes de eliminarla
        if 'Nombre completo' in df.columns:
            nombre_completo = df.pop('Nombre completo')  # Eliminamos la columna y guardamos los datos
        
        # Verificar si la columna existe antes de eliminarla
        if 'Fecha' in df.columns:
            fecha = df.pop('Fecha')  # Eliminamos la columna y guardamos los datos
        

        df = df.fillna(df.mean())

        try:
            # Guardar los valores originales
            original_1er_sem = df['Materias 1er sem (calificacion)'].copy()
            original_2do_sem = df['Materias 2do sem (calificacion)'].copy()

            # Multiplicar por 2 (proceso temporal)
            df['Materias 1er sem (calificacion)'] *= 2
            df['Materias 2do sem (calificacion)'] *= 2

            # Iniciar prediccion
            predictions = model.predict(df)
            probabilities = model.predict_proba(df)[:, 1]

            df['Desercion'] = ['Si' if p == 0 else 'No' for p in predictions]
            df['Probabilidad de Desercion'] = 1 - probabilities
            df['Probabilidad de No Desercion'] = probabilities

            # Crear gráfico de barras
            desercion_counts = df['Desercion'].value_counts()
            plt.figure(figsize=(6, 4))
            desercion_counts.plot(kind='bar', color=['#ff416c', '#7abfdf'])

            plt.title('Probabilidad de Desertar vs Probabilidad de no Desertar')
            plt.xlabel('Deserción')
            plt.ylabel('Cantidad')
            plt.xticks(rotation=0)

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

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

            # Restaurar los valores originales antes de guardar
            df['Materias 1er sem (calificacion)'] = original_1er_sem
            df['Materias 2do sem (calificacion)'] = original_2do_sem

            # Verificar si la variable fue creada antes de reinsertarla
            if 'nombre_completo' in locals():
              df.insert(0, 'Nombre completo', nombre_completo)  # Reinsertar en la posición original

            # Verificar si la variable fue creada antes de reinsertarla
            if 'fecha' in locals():
              df['Fecha'] = fecha  # Agregar al final del DataFrame   
           
            # 📌 Guardar el archivo XLSX
            output_path = 'static/predicciones.xlsx'
            df.to_excel(output_path, index=False)

            # Obtener el nombre original del archivo subido (sin extensión .xlsx)
            original_filename = file.filename
            base_filename = os.path.splitext(original_filename)[0]

           
            s3_key = f"imagenesXLXS_s3/{base_filename}.png"
            s3_client.put_object(Body=img, Bucket=BUCKET_NAME, Key=s3_key, ContentType='image/png')
            
            # Subir archivo XLXS a S3 con el nombre original
            s3_key = f"archivosXLXS_s3/{original_filename}"  # Guardar en la carpeta "archivos_s3" con el nombre original
            s3_client.upload_file(output_path, BUCKET_NAME, s3_key)

            img_b64 = base64.b64encode(img.getvalue()).decode('utf-8')

            return render_template('cargarDatos.html', archivo_generado=True, img_b64=img_b64)

        except NotFittedError:
            return render_template('cargarDatos.html', mensaje_error="El modelo no está entrenado.")
        except ValueError:
            return render_template('cargarDatos.html', mensaje_error="Error en los datos: XLSX con formato incorrecto.")
        except Exception as e:
            print(f"Error general: {str(e)}")
            return render_template('cargarDatos.html', mensaje_error="Error en el archivo XLSX.")

    except Exception as e:
        print(str(e))
        return render_template('cargarDatos.html', mensaje_error="Error en el archivo XLSX.")

@xlsx_bp.route('/descargar_xlsx')
@login_required
def descargar_xlsx():
    """ Descarga el XLSX generado """
    output_path = 'static/predicciones.xlsx'
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return "No hay archivo disponible para descargar", 404