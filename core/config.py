import os
from dotenv import load_dotenv
    
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ENV = os.getenv('ENV')
TESTING=(True if ENV == 'development' else False)
DEBUG=(True if ENV == 'development' else False)
