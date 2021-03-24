from enum import unique
from peewee import Model, AutoField, CharField, BigAutoField, DateField, DateTimeField, DecimalField, ForeignKeyField
from datetime import datetime

from core.db import DB

banco = DB().configure()

class CleverBaseModel(Model):
    created = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = banco


class Ativo(CleverBaseModel):

    id = AutoField(index_type='BRIN')
    simbolo = CharField(max_length=50, unique=True)
    nome = CharField(max_length=100)
    pais = CharField(max_length=50)


class HistoricalData(CleverBaseModel):

    id = BigAutoField(index_type='BRIN')
    data_historico = DateField()
    ultimo = DecimalField(decimal_places=2)
    variacao = DecimalField(decimal_places=4)
    ativo = ForeignKeyField(Ativo, backref='historicos')

def initialize():
    banco.connect()
    banco.create_tables([Ativo, HistoricalData], safe=True)
