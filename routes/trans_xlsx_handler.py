from flask import Blueprint, request, render_template, send_file
import pandas as pd
import os
from sklearn.exceptions import NotFittedError
import utils.diccionario_handler as dh
from utils.decorators import login_required

trans_xlsx_bp = Blueprint('trans_xlsx_handler', __name__)



@trans_xlsx_bp.route('/trans_procesar_xlsx', methods=['POST'])
@login_required
def trans_procesar_xlsx():
    """ Procesa el archivo XLSX """
    try:
        file = request.files['archivo_xlsx']
        if not file or not file.filename.endswith('.xlsx'):
            return render_template('transformarDatos.html', mensaje_error="Debe ser un archivo XLSX válido")

        #df = pd.read_excel(file) 
        df = pd.read_excel(file, engine='openpyxl') # 📌 Ahora leemos archivos XLSX
        if df.empty:
            return render_template('transformarDatos.html', mensaje_error="El archivo XLSX está vacío")
         
        # Verificar si la columna existe antes de eliminarla
        if 'Nombre completo' in df.columns:
            nombre_completo = df.pop('Nombre completo')  # Eliminamos la columna y guardamos los datos

        # Verificar si la columna existe antes de eliminarla
        if 'Fecha' in df.columns:
            fecha = df.pop('Fecha')  # Eliminamos la columna y guardamos los datos    

        # Validar cantidad exacta de columnas
        NUMERO_CORRECTO_COLUMNAS = 25
        if df.shape[1] != NUMERO_CORRECTO_COLUMNAS:
            return render_template('transformarDatos.html', mensaje_error=f"El archivo debe tener exactamente {NUMERO_CORRECTO_COLUMNAS} columnas.")

        # Validar que solo las 25 columnas tengan datos
        columnas_con_datos = df.dropna(how='all', axis=1).shape[1]
        if columnas_con_datos != NUMERO_CORRECTO_COLUMNAS:
            return render_template('transformarDatos.html', mensaje_error="El archivo tiene columnas vacías o adicionales con datos.")

        # Verificar si el archivo ya tiene números o texto en ciertas columnas nnnnnnnnnnnnnnnnnnn
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

        # Verificar si la variable fue creada antes de reinsertarla
        if 'nombre_completo' in locals():
           df.insert(0, 'Nombre completo', nombre_completo)  # Reinsertar en la posición original
         
        # Verificar si la variable fue creada antes de reinsertarla
        if 'fecha' in locals():
            df['Fecha'] = fecha  # Agregar al final del DataFrame   
          
         
        # Guardar el archivo XLSX transformado
        output_path = 'static/transformado.xlsx'
        df.to_excel(output_path, index=False)

        return render_template('transformarDatos.html', archivo_generado=True)

    except NotFittedError:
        return render_template('transformarDatos.html', mensaje_error="ERROR")
    except ValueError:
        return render_template('transformarDatos.html', mensaje_error="Error en los datos: XLSX con formato incorrecto.")
    except Exception as e:
        print(f"Error general: {str(e)}")
        return render_template('transformarDatos.html', mensaje_error="Error en el archivo XLSX.")

@trans_xlsx_bp.route('/descargar_trans_xlsx')
@login_required
def descargar_trans_xlsx():
    """ Descarga el XLSX generado """
    output_path = 'static/transformado.xlsx'
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return "No hay archivo disponible para descargar", 404