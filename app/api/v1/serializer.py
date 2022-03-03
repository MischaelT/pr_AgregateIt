from currency.models import ContactUs, Rate, Source
from currency.tasks import send_email

from rest_framework import serializers

# Валидация и способ отдачи данных


class RelatedRateSerializer(serializers.ModelSerializer):

    """
        Serializer for related rates
    """

    class Meta:
        model = Rate
        fields = (
            'ask',
            'bid',
            'currency_name',
            'created',
        )


class SourceSerializer(serializers.ModelSerializer):

    """
        Serializer for sources
    """

    related_rates = RelatedRateSerializer(many=True, read_only=True, source='rates')

    class Meta:
        model = Source
        fields = (
            'id',
            'name',
            'related_rates',
        )


class RelatedSourceSerializer(serializers.ModelSerializer):

    """
        Serializer for related sources
    """

    class Meta:
        model = Source
        fields = (
            'id',
            'name',
        )


class RateSerializer(serializers.ModelSerializer):

    """
        Serializer for rates
    """

    #  Вложенный объект
    #  Джанго не умеет записывать вложенные объекты, поэтому мы ставим рид онли тру,
    #  чтобы оно сработало только на гет запрос
    source_obj = RelatedSourceSerializer(source='source', read_only=True)

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


class ContactUsSerializer(serializers.ModelSerializer):

    """
        Serializer for contat us lists
    """

    class Meta:
        model = ContactUs
        fields = (
            'id',
            'email_from',
            'subject',
            'message',
            'created',
        )

    def create(self, validated_data):
        subject = validated_data['subject']
        recipient = validated_data['email_from']

        full_email = 'Thank you for your message. We will write you in two working days'

        send_email.apply_async(args=(subject, full_email, recipient))
        # send_email(subject=subject, full_email=full_email, recipient_list=[recipient])

        return super().create(validated_data)
