# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse  #**para retornar uma escopo simples ao usuário
from django.contrib.messages import constants #**para realizar as importações dos dados passados, como o login
from django.contrib.auth.models import User  
#**User é uma classe do python que presenta uma tabela do banco 
from django.contrib.messages import constants
from django.contrib import messages 
from django.contrib import auth

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')  #**comando get pega o dicionário
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if not senha == confirmar_senha:  #**para validação da senha
            messages.add_message(request, constants.ERROR, 'Os campos não coincidem!')
            return redirect('/usuarios/cadastro') #**caso o usuário erre a senha, eu mando pra tela de cadastro novamente
        
        user = User.objects.filter(username=username) 
                  #****User é uma tabela do banco de dados já criada pelo django
        if user.exists(): #**se não for vazio, ou seja, se retornar o nome que já existe; ele retorna pra tela de cadastro de novo
            messages.add_message(request, constants.ERROR, 'Usuário já existe!')
            return redirect('/usuarios/cadastro') #**irá verificar se já existe o usarname digitado no banco
        
        try:
            user = User.objects.create_user(   #**create_user, função já criada pelo django
                username=username,   #**à esquerda é a coluna da nossa tabela
                password=confirmar_senha, #**no direito o valor inserido que foi digitado pelo usuário
            )

            return redirect('/usuarios/logar')
        
        except:
            messages.add_message(request, constants.ERROR, 'Erro no servidor!')
            return redirect('/usuarios/cadastro')


def logar(request):
    if request.method == 'GET': #**recebe o nome do arquivo (com o caminho dele caso precise)
        print(request.user)
        return render(request, 'login.html')  #**render recebe pelo menos 2 parâmetros
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
                                        #**coluna do banco=variável, o que é digitado 
        user = auth.authenticate(request, username=username, password=senha)
        #**o user, só verifica que o usário existe
        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logado!') #**quando logar
            return redirect('/novoprojeto/novo_novoprojeto/') #**usuário é direcionado para essa página
        else:
            messages.add_message(
                request, constants.ERROR, 'Usuário ou senha inválidos'
            )
            return redirect('/usuarios/logar/') 
        

def logout(request):
    auth.logout(request)
    return redirect('/usuarios/logar')