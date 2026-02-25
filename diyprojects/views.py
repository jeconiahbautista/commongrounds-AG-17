from django.shortcuts import render

def diyprojects_list(request):
    return render(request, 'diy-projects_list.html')