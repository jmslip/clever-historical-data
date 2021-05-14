from flask import Flask
from flask_restplus import Api


class Server:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.app.config.from_pyfile('config.py')
        self.api = Api(
            self.app,
            version='0.1.0',
            title='Clever Historical Data',
            description='Api para realizar atualização de dados históricos dos ativos (Mercado financeiro)',
            doc='/docs'
        )
    
    def run(self):
        self.app.run()


server = Server()