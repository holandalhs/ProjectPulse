from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .models import Apostila, ViewApostila
from django.contrib.messages import constants ##**trabalhando com mensagens 
from django.contrib import messages 

# Create your views here.
def adicionar_apostilas(request):
    if request.method == 'GET':
        apostilas = Apostila.objects.filter(user=request.user)
        #**contabiliza quantos acessos teve à determinada apostila do usuário 
        views_totais = ViewApostila.objects.filter(apostila__user = request.user).count()

        return render(request, 'adicionar_apostilas.html', {'apostilas': apostilas, 'views_totais': views_totais})
    
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        arquivo = request.FILES['arquivo'] #**os arquivos vem com um atributo próprio FILES, não usa get/post 

        apostila = Apostila(user=request.user, titulo=titulo, arquivo=arquivo)
        apostila.save()
        messages.add_message(
            request, constants.SUCCESS, 'Apostila adicionada com sucesso.'
        )
        return redirect('/apostilas/adicionar_apostilas/')
    

def apostila(request, id):
    apostila = Apostila.objects.get(id=id)
    views_unicas = ViewApostila.objects.filter(apostila=apostila).values('ip').distinct().count()
    views_totais = ViewApostila.objects.filter(apostila=apostila).count()

    print(views_totais)
    print(views_unicas)

    ##**view- instância da class ViewApostila 
    view = ViewApostila(
    ip=request.META['REMOTE_ADDR'],  ##**pega o ip do acesso à apostila 
    apostila=apostila)
    view.save()

    ##**renderizar o html 
    return render(request, 'apostila.html', 
                  {'apostila': apostila, 
                   'views_unicas':views_unicas, 
                   'views_totais':views_totais})


