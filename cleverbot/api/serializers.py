from rest_framework import serializers
from cleverbot import models


class HistoricalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HistoricalData
        fields = '__all__'