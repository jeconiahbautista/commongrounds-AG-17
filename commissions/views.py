from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView

from .models import CommissionType, Commission

def index(request):
    return HttpResponse('Hello! This is the Commissions Requests Apps.')

def request_list(request):

    commissions = Commission.objects.all()
    ctx = {
        'commissions' : commissions
    }

    return render(request, "commissions/request_list.html", ctx)

class RequestListView(ListView):
    model = Commission
    template_name = 'commissions/request_list.html'



