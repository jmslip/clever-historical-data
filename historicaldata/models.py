from django.db import models

class Ativo(models.Model):
    nome = models.CharField('Nome', max_length=100)
    simbolo = models.SlugField('Símbolo', max_length=100)
    created = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Ativo'
        verbose_name_plural = 'Ativos'
        ordering = ['nome']


class HistoricalData(models.Model):
    data_historico = models.DateTimeField('Data')
    ultimo = models.FloatField('Último')
    variacao = models.FloatField('Var%')
    ativo = models.ForeignKey(Ativo, verbose_name='Ativo', on_delete=models.CASCADE)
    created = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Dado Histórico'
        verbose_name_plural = 'Dados Históricos'
        ordering = ['data_historico', 'ativo']
