from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
import re
from database.bd import get_user_by_username, create_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        account = get_user_by_username(username)

        if account and check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['rol'] = account['rol']
            return redirect(url_for('home.home'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and all(k in request.form for k in ['username', 'password', 'email']):
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        account = get_user_by_username(username)
        
        if account:
            flash('¡La cuenta ya existe!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('¡Dirección de correo electrónico no válida!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('¡El nombre de usuario solo debe contener letras y números!')
        else:
            hashed_password = generate_password_hash(password)
            create_user(fullname, username, hashed_password, email)
            flash('¡Te has registrado con éxito!')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
def profile():
    if 'loggedin' in session:
        account = get_user_by_username(session['username'])
        return render_template('auth/profile.html', account=account)
    return redirect(url_for('auth.login'))