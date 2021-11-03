from django.urls import path
from django.urls.resolvers import URLPattern
from .views import inicio, peticiones,ayuda,resumen,rango

urlpatterns = [
    path('carga',inicio),
    path('peticiones',peticiones),
    path('ayuda',ayuda),
    path('resumen',resumen),
    path('rango',rango),
]
