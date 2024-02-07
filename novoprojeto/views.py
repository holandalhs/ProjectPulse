from django.shortcuts import render, redirect 
from .models import Categoria, Situacao, Novoprojeto, Recurso   ##, Notificacao
from django.http import HttpResponse
from django.contrib.messages import constants
from django.contrib import messages

from django.shortcuts import render
from django.template.loader import get_template
#from xhtml2pdf import pisa
#import xlwt

#**para acessasr um atributo de classe, no caso a CATEGORIA que está no models.py, importe a classe
#**e crie uma nova variável para acessar os seus dados, variável 'dificuldades'

# Create your views here.
def novo_projeto(request):
    if not request.user.is_authenticated: #**se não estiver autenticado, retorna false; e é redirecionado
        return redirect('/usuarios/logar')
    #**se estiver logado, retorna true e nada acontece

    #**vou no bd busco os dados cadastrados para que o usuário possa optar por qual cadastrar
    if request.method == 'GET': #***GET estou puxando as informações, acessando o servidor 
        categorias = Categoria.objects.all() #**.all trago todas as categorias cadastradas no banco
        situacoes = Situacao.objects.all()
        dificuldades = Novoprojeto.DIFICULDADE_CHOICES
        recursos = Recurso.objects.all()
       
        
        #**PARA LISTAR OS PROJETOS DINAMICAMENTE
        #**PRECISO BUSCAR DO BD OS PROJETOS, UTILIZANDO A MODEL novoprojeto****************** 
        #**objects PARA ACESSAR OS DADOS DO BANCO E FILTRAR POR
        novoprojeto = Novoprojeto.objects.filter(user=request.user) #**essa variável contem todos os dados enviados do projeto
                                            #**PARA ESSE USUÁRIO ESPECÍFICO-LOGADO
        #***em 1h v2
        #******************************************************************************************
        #**********BUSCAR OS DADOS QUE FORAM ENVIADOS PELO FORMULÁRIO novo_projeto.html************
        #**buscar os dados que foram enviados pelo método GET para o formulário/projeto em models.py
        categoria_filtrar = request.GET.get('categoria')   
        situacao_filtrar = request.GET.get('status') 
        dificuldade_filtrar = request.GET.get('dificuldade')  
        recurso_filtrar = request.GET.get('tiporecurso')
        #data_lancamento_filtrar = request.GET.get('lancamento')
        #**mesmo nome que estar no método GET do arquivo novo_projeto.html *********IMPORTANTE

        if categoria_filtrar:
            novoprojeto = novoprojeto.filter(categoria__id=categoria_filtrar)

        if situacao_filtrar:
            novoprojeto = novoprojeto.filter(situacao__id=situacao_filtrar)
        #****por que tenho que passar situacao__id e não status como está o nome no arquivo novo_projeto.html???

        if dificuldade_filtrar:
            novoprojeto = novoprojeto.filter(dificuldade=dificuldade_filtrar)

        if recurso_filtrar:
            novoprojeto = novoprojeto.filter(recurso__id=recurso_filtrar)
       

     
        return render(request, 'novo_projeto.html',   #***em 25' v2
        {
            'categorias': categorias,
            'situacoes': situacoes,
            'dificuldades': dificuldades,
            'recursos': recursos, 
            #'data_lancamento': data_lancamento,
            #'data_encerramento': data_encerramento,
            'novoprojeto': novoprojeto,
        })        
                          #**buscando os dados do html 
    elif request.method == 'POST': #**verificando se os dados foram enviados, para recebê-los aqui
        titulo = request.POST.get('titulo')   #**variável criada = estou buscando da minha requisição com
        escopo = request.POST.get('escopo')  #**o método post o valor com o name 'titulo' do novo_projeto.html
        observacao = request.POST.get('observacao')

        data_lancamento = request.POST.get('data_inicio')
        data_encerramento = request.POST.get('data_fim')

        ###notificacao = request.POST.get('notificacao')
        orcamento = request.POST.get('orcamento')


        categoria = request.POST.get('categoria')
        situacao = request.POST.get('situacao')
        dificuldade = request.POST.get('dificuldade')
        recurso = request.POST.get('recurso')

            

        #**tratativa para verificar se houve preenchimento dos campos título e escopo pelo usuário
        #***tratativa de erro
        if len(titulo.strip()) == 0 or len(escopo.strip()) == 0: #**strip verifica se está vazio ou com espaços
            messages.add_message(
                request,
                constants.ERROR,
                'Preencha os campos de título e escopo',
            )
            return redirect('/novoprojeto/novo_projeto/')

        novo = Novoprojeto(   #**criei uma variável  e estou instanciando com a classe principal Novoprojeto 
            user=request.user,  #**o usuário desse projeto é o próprio usuário logado!

            titulo=titulo,  #**variável criada que recebe titulo citado no elip linha 31 
            escopo=escopo,
            observacao=observacao,

            data_lancamento=data_lancamento,
            data_encerramento=data_encerramento,
            ##notificacao=notificacao,
            orcamento=orcamento,


            categoria_id=categoria, #**com o _id ao invés de passar uma instância da categoria... passo logo o id e não a instância de categoria                                   
            situacao_id=situacao,   #**sempre que tiver uma chave estrangeira faço isso
            dificuldade=dificuldade,
            recurso_id=recurso,
                                    #**até aqui não fica salvo no banco de dados- cria apenas uma 
                                    #**representação do projeto na memória              
            
            
        )            #**o método save salva no banco, commit               
        novo.save()  #**commitando, levando pro gerenciador do banco e salvando os dados 
                        #**a variável novoprojeto recebe uma instancia de models.py
                
        messages.add_message(
            request, constants.SUCCESS, 'Projeto criado com sucesso'
        )
        return redirect('/novoprojeto/novo_projeto')



