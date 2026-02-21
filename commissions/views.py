from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello! This is the Commissions Requests Apps.')

# Create your views here.
