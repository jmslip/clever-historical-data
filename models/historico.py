from datetime import datetime
from core.db import db

class HistoricalData(db.Model):
    __tablename__ = 'historical_data'

    id = db.Column(db.Integer, primary_key=True)
    data_historico = db.Column(db.Date, nullable=False)
    ultimo = db.Column(db.Float, nullable=False)
    variacao = db.Column(db.Float, nullable=False)
    created = db.Colum(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, data_historico, ultimo, variacao) -> None:
        self.data_historico = data_historico
        self.ultimo = ultimo
        self.variacao = variacao
        self.created = datetime.utcnow

    def json(self):
        return {
            'data_historico': self.data_historico,
            'ultimo': self.ultimo,
            'variacao': self.variacao,
            'data_criacao': self.created
        }