from django.http.response import HttpResponse
from django.shortcuts import render

def hello_world(request):
    return HttpResponse('Hello world')


