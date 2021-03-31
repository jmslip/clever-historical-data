from peewee import IntegerField, Model, CharField, BigAutoField, DateField, DateTimeField, DecimalField, ForeignKeyField
from datetime import datetime

from core.db import DB

banco = DB().configure()

class CleverBaseModel(Model):
    created = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = banco


class Ativo(CleverBaseModel):

    id = IntegerField(primary_key=True)
    simbolo = CharField(max_length=50, unique=True, index=True)
    nome = CharField(max_length=100)
    pais = CharField(max_length=50)


class HistoricalData(CleverBaseModel):

    id = BigAutoField(index_type='BRIN')
    data_historico = DateField()
    variacao = DecimalField(decimal_places=4)
    ativo = ForeignKeyField(Ativo, backref='historicos')

    class Meta:
        indexes = (
            # cria index para data/ativo
            (('data_historico', 'ativo'), True),
        )

def initialize():
    banco.connect()
    banco.create_tables([Ativo, HistoricalData], safe=True)


def close_connection():
    banco.close()
