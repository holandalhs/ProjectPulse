from django.urls import path
from . import views #** o . pra informar que da pasta novoprojeto vou importar a views

urlpatterns = [
    path('novo_projeto/', views.novo_projeto, name='novo_projeto'),
    path('deletar_projeto/<int:id>', views.deletar_projeto, name='deletar_projeto'),
    path('consultar_projeto/', views.consultar_projeto, name='consultar_projeto'),
    path('listar_projeto/', views.listar_projeto, name='listar_projeto'),

    ##**listando os projetos do Ambiente 
    path('listagem/<int:id>/', views.listagem, name='listagem'), #**chamada em listar_projeto.html 53
    path('executar_projeto/<int:id>/', views.executar_projeto, name='executar_projeto'),

    path('relatorio/<int:id>/', views.relatorio, name='relatorio'), #**recebe o id do Home
    #**o caminho da url que chamo, chama a função views do python novo_projeto, name da url
]