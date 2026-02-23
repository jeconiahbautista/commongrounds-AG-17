from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Commission

def index(request):
    return HttpResponse('Hello! This is the Commissions Requests Apps.')

def commission_list(request):
    commissions = Commission.objects.all()
    ctx = {
        'commissions' : commissions
    }

    return render(request, "commissions/request_list.html", ctx)

def commission_detail(request, id):
    ctx = { 'commissions', Commission.objects.get(id=id) }
    return render(request, 'commissions/commission_detail.html', ctx)

class CommissionListView(ListView):
    model = Commission

class CommissionDetailView(DetailView):
    model = Commission
    context_object_name = 'commission'
    



