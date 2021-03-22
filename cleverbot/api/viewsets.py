from rest_framework import viewsets
from cleverbot.api import serializers

from cleverbot import models


class HistoricalDataViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HistoricalDataSerializer
    queryset = models.HistoricalData.objects.all()