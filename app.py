from flask import Flask
from config import Config
import os

# Crear la app
app = Flask(__name__)
app.config.from_object(Config)

# Importar los blueprints y la base de datos
from routes.auth import auth_bp
from routes.routes import home_bp  # <-- cambia esta línea
from routes.traerS3_lista import traerS3r_bp
from routes.chatbot_handler import chatbot_bp
from routes.predict import predict_bp
from routes.descargarDynamo_handler import descargarDynamo_bp
from routes.xlsx_handler import xlsx_bp
from routes.csv_handler import csv_bp
from routes.trans_xlsx_handler import trans_xlsx_bp
from routes.trans_csv_handler import trans_csv_bp


from database import bd

# Inicializar extensiones y registrar blueprints
bd.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(traerS3r_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(descargarDynamo_bp)
app.register_blueprint(xlsx_bp)
app.register_blueprint(csv_bp)
app.register_blueprint(trans_xlsx_bp)
app.register_blueprint(trans_csv_bp)

# Ejecutar la app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))