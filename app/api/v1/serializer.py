from rest_framework import serializers

from currency.models import Rate

# Валидация и способ отдачи данных

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'ask',
            'bid',
            'currency_name',
            'source_id',
            'created',
        )

