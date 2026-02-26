from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Commission


class CommissionListView(ListView):
    model = Commission


class CommissionDetailView(DetailView):
    model = Commission
    context_object_name = 'commission'
    



