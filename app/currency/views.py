from currency.models import ContactUs

from django.http.response import HttpResponse


def hello_world(request):
    return HttpResponse('Hello world')


def get_contact_us(request):
    contactUs_objects = ContactUs.objects.all()
    result = []

    for item in contactUs_objects:
        result.append(
            f'From: {item.email_from}, Topic: {item.subject}, Text: {item.message} <br> <br>'
        )

    return HttpResponse(result)


"""
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
"""
