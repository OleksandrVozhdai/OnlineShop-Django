from django.http import HttpResponse
from django.shortcuts import render

def IndexView(request):
    return render(request, 'main/index.html')

# Create your views here.
