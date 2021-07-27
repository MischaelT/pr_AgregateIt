from currency.forms import RateForm, SourceForm
from currency.models import ContactUs, Rate, Source

from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


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


def create_rate(request):

    if request.method == 'POST':

        form = RateForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/rate/list/')

    elif request.method == 'GET':
        form = RateForm()

    context = {
        'form': form,
    }

    return render(request, 'create_rate.html', context=context)


def delete_rate(request, rate_id):
    rate = get_object_or_404(Rate, id=rate_id)

    if request.method == 'POST':
        rate.delete()
        return HttpResponseRedirect('/rate/list/')

    context = {
        'object': rate,
    }

    return render(request, 'delete_rate.html', context=context)


def update_rate(request, rate_id):
    rate = get_object_or_404(Rate, id=rate_id)

    if request.method == 'POST':
        # форма заполняется данными, которые уже есть в БД
        form = RateForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/rate/list/')
    elif request.method == 'GET':
        form = RateForm(instance=rate)

    context = {
        'form': form,
    }

    return render(request, 'update_rate.html', context=context)


def get_rate_details(request, rate_id):

    rate = get_object_or_404(Rate, id=rate_id)
    context = {
        'object': rate,
    }
    return render(request, 'rate_details.html', context=context)


def source_list(request):

    source_objects = Source.objects.all()

    context = {'source_list': source_objects}

    return render(request, 'source_list.html', context=context)


def create_source(request):

    if request.method == 'POST':

        form = SourceForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')

    elif request.method == 'GET':
        form = SourceForm()

    context = {
        'form': form,
    }

    return render(request, 'create_source.html', context=context)


def delete_source(request, source_id):
    source = get_object_or_404(Source, id=source_id)

    if request.method == 'POST':
        source.delete()
        return HttpResponseRedirect('/source/list/')

    context = {
        'object': source,
    }

    return render(request, 'delete_source.html', context=context)


def update_source(request, source_id):
    source = get_object_or_404(Source, id=source_id)

    if request.method == 'POST':
        # форма заполняется данными, которые уже есть в БД
        form = SourceForm(request.POST, instance=source)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')
    elif request.method == 'GET':
        form = SourceForm(instance=source)

    context = {
        'form': form,
    }

    return render(request, 'update_source.html', context=context)


def get_source_details(request, source_id):

    source = get_object_or_404(Source, id=source_id)
    context = {
        'object': source,
    }
    return render(request, 'source_details.html', context=context)
