from flask import Blueprint, render_template, redirect, url_for, session, g
from utils.decorators import admin_required, login_required

home_bp = Blueprint('home', __name__)

# Código para obtener el username desde la sesión
@home_bp.before_request
def before_request():
    g.username = session.get('username')  # Obtiene el username desde la sesión

@home_bp.route('/')
def home():
    return render_template('index.html')  # Usa g.username en la plantilla si es necesario
 

# @home_bp.route('/')
# def home():
#     username = session.get('username')  # Por si está logueado, pasamos el username
#     return render_template('index.html', username=username)

# @home_bp.route('/')
# def home():
#     if 'loggedin' in session:
#         return render_template('home.html', username=session['username'])
#     return redirect(url_for('auth.login'))

@home_bp.route('/formulario')
@login_required
def formulario():
    return render_template('formulario.html')

@home_bp.route('/ultimas_predicciones')
@login_required
def ultimas_predicciones():
     return redirect(url_for('traerS3_lista.traers3r'))

@home_bp.route('/chatbot_pagina')
def chatbot_pagina():
     return redirect(url_for('chatbot_handler.chatbot_page'))

#Transformar Datos
@home_bp.route('/transformar_cargarPage')
@login_required
def transformar_cargarPage():
    return render_template('transformarDatos.html', archivo_generado=False)

#Cargar Datos
@home_bp.route('/cargar_datosPage')
@login_required
def cargar_datosPage():
    return render_template('cargarDatos.html', archivo_generado=False)


#Reporte 
@home_bp.route('/descargar_ReportePage')
@admin_required
def descargar_ReportePage():
    return render_template('descargarDynamo.html', archivo_generado=False)
