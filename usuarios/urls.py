from django.urls import path    #**cria as novas urls dentro do django 
from . import views             #** from . ==indica que quero a importação na mesma pasta que estou
                                #**dentro da pasta 'usuarios' importe a pasta 'views' 
import django 

urlpatterns = [
    #**rota da url, função que é uma lista, para a chamada das funcionalidades abaixo
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logar/', views.logar, name='login'),
    
    path('logout/', views.logout, name='logout'),
]
#**lista onde as urls são cadastradas 
#**nesse ponto são chamadas as funções para 'usuarios'