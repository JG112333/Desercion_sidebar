from flask import Blueprint, request, render_template, send_file
import pandas as pd
import os
from sklearn.exceptions import NotFittedError
import utils.diccionario_handler as dh
from utils.decorators import login_required

trans_csv_bp = Blueprint('trans_csv_handler', __name__)

@trans_csv_bp.route('/trans_procesar_csv', methods=['POST'])
@login_required
def trans_procesar_csv():
    """ Procesa el archivo CSV """
    try:
        file = request.files['archivo_csv']
        if not file or not file.filename.endswith('.csv'):
            return render_template('transformarDatos.html', mensaje_error="Debe ser un archivo CSV válido")

        df = pd.read_csv(file, encoding="utf-8-sig")
        print(df.columns.tolist())

        if df.empty:
            return render_template('transformarDatos.html', mensaje_error="El archivo CSV está vacío")
        
        # 📌 Guardar y eliminar la columna "Nombre completo" si existe
        if 'Nombre completo' in df.columns:
            nombre_completo = df.pop('Nombre completo')  # Elimina y guarda la columna

        # Verificar si la columna existe antes de eliminarla
        if 'Fecha' in df.columns:
            fecha = df.pop('Fecha')  # Eliminamos la columna y guardamos los datos    
        
        # 📌 Validación 1: El archivo debe tener exactamente 25 columnas
        if df.shape[1] != 25:
            return render_template('transformarDatos.html', mensaje_error="Error: El archivo debe contener exactamente 26 columnas.")

        # 📌 Validación 2: Todas las columnas deben tener datos (sin columnas con valores nulos o vacíos)
        if df.isnull().any().any():
            return render_template('transformarDatos.html', mensaje_error="Error: El archivo tiene columnas con valores vacíos o nulos.")

        # 📌 Validación 3: No deben existir filas con menos de 25 valores llenos
        if (df.count(axis=1) != 25).any():
            return render_template('transformarDatos.html', mensaje_error="Error: Algunas filas no tienen los 26 valores completos.")



        # Verificar si el archivo ya tiene números o texto en ciertas columnas
        es_numerico = df['Estado civil'].apply(lambda x: isinstance(x, (int, float))).all()

        if es_numerico:
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
        else:
            # Convertir texto a números
            df['Estado civil'] = df['Estado civil'].map(dh.estado_civil_map)
            df['Modo de admision'] = df['Modo de admision'].map(dh.modo_admision_map)
            df['Asistencia diurna o nocturna'] = df['Asistencia diurna o nocturna'].map(dh.asistencia_map)
            df['Cualificacion previa'] = df['Cualificacion previa'].map(dh.cualificacion_previa_map)
            df['Ocupacion de la madre'] = df['Ocupacion de la madre'].map(dh.ocupacion_madre_map)
            df['Ocupacion del padre'] = df['Ocupacion del padre'].map(dh.ocupacion_padre_map)
            df['Desplazado'] = df['Desplazado'].map(dh.desplazado)
            df['Deudor'] = df['Deudor'].map(dh.deudor)
            df['Cuotas de matricula al dia'] = df['Cuotas de matricula al dia'].map(dh.matricula_al_dia)
            df['Genero'] = df['Genero'].map(dh.genero)
            df['Becado'] = df['Becado'].map(dh.becado)

        # 📌 Volver a insertar la columna en la posición original (al inicio)
        if 'nombre_completo' in locals():
            df.insert(0, 'Nombre completo', nombre_completo)  # Reinsertar en la primera posición

        # Verificar si la variable fue creada antes de reinsertarla
        if 'fecha' in locals():
            df['Fecha'] = fecha  # Agregar al final del DataFrame     

        # Guardar el archivo CSV transformado
        output_path = 'static/transformado.csv'
        df.to_csv(output_path, index=False, encoding="utf-8-sig")

        return render_template('transformarDatos.html', archivo_generado=True)
        #return send_file(output, mimetype='text/csv', as_attachment=True, download_name='datos_transformados.csv')
    except NotFittedError:
        return render_template('transformarDatos.html', mensaje_error="ERROR")
    except ValueError:
        return render_template('transformarDatos.html', mensaje_error="Error en los datos: CSV con formato incorrecto.")
    except Exception as e:
        print(f"Error general: {str(e)}")
        return render_template('transformarDatos.html', mensaje_error="Error en el archivo CSV.")
    
@trans_csv_bp.route('/descargar_trans_csv')
@login_required
def descargar_trans_csv():
    """ Descarga el CSV generado """
    output_path = 'static/transformado.csv'
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return "No hay archivo disponible para descargar", 404