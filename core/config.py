import os
from dotenv import load_dotenv
    
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_ADDR = os.getenv('DB_ADDR')
SECRET_KEY = os.getenv('SECRET_KEY')
ENV = os.getenv('ENV')
