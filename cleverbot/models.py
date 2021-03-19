from django.db import models

class HistoricalData(models.Model):
    data_historico = models.DateTimeField('Data')
    ultimo = models.FloatField('Último')
    variacao = models.FloatField('Var%')
    ativo = models.CharField('Ativo', max_length=100)
    created = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Dado Histórico'
        verbose_name_plural = 'Dados Históricos'
        ordering = ['data_historico', 'ativo']
