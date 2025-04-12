import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_REGION2 = os.getenv('AWS_REGION2')
AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')
AWS_DYNAMODB_TABLE = os.getenv('AWS_DYNAMODB_TABLE')
GEMINI = os.getenv("GEMINI")

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')