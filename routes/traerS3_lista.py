from flask import Blueprint, render_template
import boto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET, AWS_REGION2
from utils.decorators import admin_required

# Configurar el cliente de S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,  
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,  
    region_name=AWS_REGION2 
)

BUCKET_NAME = AWS_S3_BUCKET

traerS3r_bp = Blueprint('traerS3_lista', __name__)

# Ruta para listar los archivos de S3
@traerS3r_bp.route('/traerS3r')
@admin_required
def traers3r():
    archivos = listar_archivos_en_s3(BUCKET_NAME)
    return render_template('listar.html', archivos=archivos)

# Función para listar archivos en el bucket de S3
def listar_archivos_en_s3(BUCKET_NAME):
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        objetos = response.get('Contents', [])

        imagenes_csv = {}
        imagenes_xlsx = {}
        archivos_csv = {}
        archivos_xlsx = {}

        for obj in objetos:
            key = obj['Key']
            url = s3_client.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': key})
            
            if key.startswith("imagenesCSV_s3/") and key.endswith(".png"):
                base_name = key.replace("imagenesCSV_s3/", "").replace(".png", "")
                imagenes_csv[base_name] = url
            elif key.startswith("imagenesXLXS_s3/") and key.endswith(".png"):
                base_name = key.replace("imagenesXLXS_s3/", "").replace(".png", "")
                imagenes_xlsx[base_name] = url
            elif key.startswith("archivosCSV_s3/") and key.endswith(".csv"):
                base_name = key.replace("archivosCSV_s3/", "").replace(".csv", "")
                archivos_csv[base_name] = url
            elif key.startswith("archivosXLXS_s3/") and key.endswith(".xlsx"):
                base_name = key.replace("archivosXLXS_s3/", "").replace(".xlsx", "")
                archivos_xlsx[base_name] = url

        # Emparejar imágenes con sus archivos
        lista_resultado = []
        nombres_base = set(imagenes_csv.keys()) | set(imagenes_xlsx.keys()) | set(archivos_csv.keys()) | set(archivos_xlsx.keys())
        
        for base_name in nombres_base:
            lista_resultado.append({
                'nombre': base_name,
                'imagen_csv_url': imagenes_csv.get(base_name),
                'imagen_xlsx_url': imagenes_xlsx.get(base_name),
                'archivo_csv_url': archivos_csv.get(base_name),
                'archivo_xlsx_url': archivos_xlsx.get(base_name)
            })
        
        return lista_resultado
    except Exception as e:
        print(f"Error al listar los archivos: {e}")
        return []