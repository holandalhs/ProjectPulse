# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse  
from django.contrib.messages import constants 
from django.contrib.auth.models import User  
from django.contrib.messages import constants
from django.contrib import messages 
from django.contrib import auth

def cadastro(request):
    ###return HttpResponse('olaaaaaaaaaaa')
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')  
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if not senha == confirmar_senha:  #**para validação da senha
            messages.add_message(request, constants.ERROR, 'Os campos não coincidem!')
            return redirect('/usuarios/cadastro') 
        
        user = User.objects.filter(username=username) 
                 
        if user.exists(): 
            messages.add_message(request, constants.ERROR, 'Usuário já existe!')
            return redirect('/usuarios/cadastro')
        
        try:
            user = User.objects.create_user(  
                username=username,  
                password=confirmar_senha, 
            )

            return redirect('/usuarios/logar')
        
        except:
            messages.add_message(request, constants.ERROR, 'Erro no servidor!')
            return redirect('/usuarios/cadastro')


def logar(request):
    if request.method == 'GET': 
        print(request.user)
        return render(request, 'login.html')  #**render recebe pelo menos 2 parâmetros
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
                                      
        user = auth.authenticate(request, username=username, password=senha)
        
        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logado!') #**quando logar
            return redirect('/novoprojeto/novo_novoprojeto/') 
        else:
            messages.add_message(
                request, constants.ERROR, 'Usuário ou senha inválidos'
            )
            return redirect('/usuarios/logar/') 
        

def logout(request):
    auth.logout(request)
    return redirect('/usuarios/logar')