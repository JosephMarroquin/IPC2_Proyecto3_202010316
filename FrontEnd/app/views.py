from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.


def inicio(request):
    return render(request, 'app/index.html')

def peticiones(request):
    return render(request, 'app/peticiones.html')

def ayuda(request):
    return render(request, 'app/ayuda.html')

def resumen(request):
    return render(request, 'app/resumen.html')
    
def rango(request):
    return render(request, 'app/rango.html')