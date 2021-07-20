from app.currency.models import Rate

from django import request
from django.http.response import HttpResponse
from django.shortcuts import render


def hello_world(request):
    return HttpResponse('Hello world')


def rate_list(requests):
    rates = Rate.objects.all()
    result = []

    for rate in rates:
        result.append(
            f'id: {rate.id} ask: {rate.ask} bid: {rate.bid}'
        )

        context = {
            'message': 'hello'
        }

    return render(request, 'rate_list.html', context=context)
