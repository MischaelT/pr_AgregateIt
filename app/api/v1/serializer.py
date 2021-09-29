from rest_framework import serializers

from currency.models import Rate, Source

# Валидация и способ отдачи данных

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            'id',
            'name',
        )

class RateSerializer(serializers.ModelSerializer):

    #  Вложенный объект
    #  Джанго не умеет записывать вложенные объекты, поэтому мы ставим рид онли тру, чтобы оно сработало только на гет запрос
    source_obj = SourceSerializer(source='source', read_only=True)
    class Meta:
        model = Rate
        fields = (
            'ask',
            'bid',
            'currency_name',
            # 'type',
            'source_obj',  # GET
            'source', 
            'created',
        )
    #  Сработает только на пост запрос 
        extra_kwargs = {
            'source': {'write_only': True},
        }

