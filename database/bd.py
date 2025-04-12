import psycopg2
import psycopg2.extras
from flask import current_app

def get_db_connection():
    return psycopg2.connect(
        dbname=current_app.config['DB_NAME'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASS'],
        host=current_app.config['DB_HOST']
    )

def init_app(app):
    # Puedes agregar inicialización de BD aquí si es necesario
    pass

# Funciones relacionadas con usuarios
def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(fullname, username, hashed_password, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (fullname, username, password, email, rol) VALUES (%s,%s,%s,%s,'Usuario')",
        (fullname, username, hashed_password, email)
    )
    conn.commit()
    conn.close()