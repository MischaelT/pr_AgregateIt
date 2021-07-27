from currency.models import ContactUs, Rate

from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def get_contact_us(request):

    contactUs_objects = ContactUs.objects.all()

    context = {'contactUs_list': contactUs_objects}

    return render(request, 'contact_us.html', context=context)


def rate_list(request):

    rates_objects = Rate.objects.all()

    context = {'rate_list': rates_objects}

    return render(request, 'rate_list.html', context=context)
