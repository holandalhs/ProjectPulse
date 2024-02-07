from django.urls import path
from . import views #** o . pra informar que da pasta novoprojeto vou importar a views

urlpatterns = [
    path('novo_projeto/', views.novo_projeto, name='novo_projeto'),
]