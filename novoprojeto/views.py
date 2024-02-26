from django.shortcuts import render, redirect 
from .models import Categoria, Situacao, Novoprojeto, Recurso, Listagem, Validacao
from django.http import HttpResponse, Http404
from django.contrib.messages import constants
from django.contrib import messages

from django.shortcuts import render
from django.template.loader import get_template

def novo_projeto(request):
    if not request.user.is_authenticated: #**se não estiver autenticado, retorna false; e é redirecionado
        return redirect('/usuarios/logar')
    #**se estiver logado, retorna true e nada acontece

    if request.method == 'GET': 
        categorias = Categoria.objects.all() 
        situacoes = Situacao.objects.all()
        dificuldades = Novoprojeto.DIFICULDADE_CHOICES
        recursos = Recurso.objects.all()
       
        
      
        novoprojeto = Novoprojeto.objects.filter(user=request.user) 
        categoria_filtrar = request.GET.get('categoria')   
        situacao_filtrar = request.GET.get('status') 
        dificuldade_filtrar = request.GET.get('dificuldade')  
        recurso_filtrar = request.GET.get('tiporecurso')
       
        if categoria_filtrar:
            novoprojeto = novoprojeto.filter(categoria__id=categoria_filtrar)

        if situacao_filtrar:
            novoprojeto = novoprojeto.filter(situacao__id=situacao_filtrar)

        if dificuldade_filtrar:
            novoprojeto = novoprojeto.filter(dificuldade=dificuldade_filtrar)

        if recurso_filtrar:
            novoprojeto = novoprojeto.filter(recurso__id=recurso_filtrar)
       

     
        return render(request, 'novo_projeto.html',  
        {
            'categorias': categorias,
            'situacoes': situacoes,
            'dificuldades': dificuldades,
            'recursos': recursos, 
            'novoprojeto': novoprojeto,
        })        
                          
    elif request.method == 'POST': 
        titulo = request.POST.get('titulo')   #**variável criada = estou buscando da minha requisição com
        escopo = request.POST.get('escopo')  #**o método post o valor com o name 'titulo' do novo_projeto.html
        observacao = request.POST.get('observacao')

        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')

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

        novo = Novoprojeto(  
            user=request.user,  

            titulo=titulo,  
            escopo=escopo,
            observacao=observacao,

            data_inicio=data_inicio,
            data_fim=data_fim,
          
            orcamento=orcamento,


            categoria_id=categoria,                
            situacao_id=situacao,   
            dificuldade=dificuldade,
            recurso_id=recurso,
                                        
            
            
        )                     
        novo.save()  #**commitando, levando pro gerenciador do banco e salvando os dados 
                        #**a variável novoprojeto recebe uma instancia de models.py
                
        messages.add_message(
            request, constants.SUCCESS, 'Projeto criado com sucesso'
        )
        return redirect('/novoprojeto/novo_projeto')

        


def deletar_projeto(request, id):  #**passo o id que é passado na função como parâmetro
    projeto = Novoprojeto.objects.get(id=id)

    projeto.delete() 
    messages.add_message(
        request, constants.SUCCESS, 'Projeto deletado com sucesso!'
    )
    return redirect('/novoprojeto/novo_projeto/') #**redirecionando para a tela de Projetos 



def consultar_projeto(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Novoprojeto.DIFICULDADE_CHOICES

        return render(
            request,
            'consultar_projeto.html',
            {'categorias': categorias, 'dificuldades': dificuldades},
        )
    elif request.method == 'POST':
        descricao_home = request.POST.get('descricao_home')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_projetos = request.POST.get('quantidade_projetos')

        listagem = Listagem(
            user=request.user,
            descricao_home=descricao_home,
            quantidade_projetos=qtd_projetos,
            dificuldade=dificuldade,
        )

        listagem.save()

        listagem.categoria.add(*categorias)  #**substituindo o for no código 

        projetos = ( 
            Novoprojeto.objects.filter(user=request.user)
            .filter(dificuldade=dificuldade)
            .filter(categoria_id__in=categorias)   
            .order_by('id') 
        )

        print(projetos.count()) #**para filtrar a qtd de projetos já lançados 

        ##usando os slices do python ****FAZENDO A VALIDAÇÃO DE QTD_PROJETOS AQUI
        if projetos.count() < int(qtd_projetos): ##**SE QTD > QUTJAREGISTRADA
            return redirect('/novoprojeto/consultar_projeto/')
            #print(f'Quantidade informada não pemitida!')
        else:
            ####****SE QTD <= QUTJAREGISTRADA PASSA
            projetos = projetos[: int(qtd_projetos)] #**vai da posição 0 até a qtd informada
            print(f'quantidade de projetos para avaliação {projetos}')

        for f in projetos:
            projeto_validacao = Validacao(
                projeto=f, 
            )
            projeto_validacao.save()
            
            listagem.projetos.add(projeto_validacao)  

        listagem.save()

       
        return redirect(f'/novoprojeto/listar_projeto/')




def listar_projeto(request):  
                              #**traz os projetos do usuário logado, o mesmo da Listagem
    ambientes = Listagem.objects.filter(user=request.user)  
   
    return render(
        request,
        'listar_projeto.html',
        {
            'ambientes': ambientes, 
        },
    )


def listagem(request, id):
    projetos_vinculados = Listagem.objects.get(id=id)   
    
    if not projetos_vinculados.user == request.user:  #**caso o ambiente não seja o meu, da http404 
        raise Http404()
        
    
    if request.method == 'GET':  #**buscando no banco 
        aprovados = projetos_vinculados.projetos.filter(executado=True).filter(aprovado=True).count()
        nao_aprovados = projetos_vinculados.projetos.filter(executado=True).filter(aprovado=False).count()
        a_avaliar = projetos_vinculados.projetos.filter(executado=False).count()
       
        return render(request, 'listagem.html', 
                      { 'projetos_vinculados': projetos_vinculados, 
                       'aprovados': aprovados, 
                       'nao_aprovados':nao_aprovados, 
                       'a_avaliar':a_avaliar },)


def executar_projeto(request, id):
    resposta_projeto = Validacao.objects.get(id=id)
    aprovado = request.GET.get('aprovado')
    
    projeto_id = request.GET.get('projeto_id')

    if not resposta_projeto.projeto.user == request.user:
        raise Http404()


    resposta_projeto.executado = True



    resposta_projeto.aprovado = True if aprovado == '1' else False
    resposta_projeto.save()
    return redirect(f'/novoprojeto/listagem/{projeto_id}/')  



def relatorio(request, id):
    detalhamento = Listagem.objects.get(id=id) #**acesso aos Ambientes

    aprovados = detalhamento.projetos.filter(aprovado=True).count()
    nao_aprovados = detalhamento.projetos.filter(aprovado=False).count()
    dados = [aprovados, nao_aprovados]


    categorias = Listagem.categoria.all()          
    name_categoria = [i.nome for i in categorias]

    dados_contagem = []  
    for categoria in categorias: 
        dados_contagem.append(detalhamento.projetos.filter(projeto__categoria=categoria).filter(aprovado=True).count()) 
    

    return render(request, 'relatorio.html', {'detalhamento': detalhamento, 'dados': dados, 'categorias': name_categoria, 'dados_contagem': dados_contagem })


