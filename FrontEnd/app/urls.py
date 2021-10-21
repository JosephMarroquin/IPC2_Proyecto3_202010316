from django.urls import path
from django.urls.resolvers import URLPattern
from .views import inicio, peticiones,ayuda

urlpatterns = [
    path('carga',inicio),
    path('peticiones',peticiones),
    path('ayuda',ayuda),
]
