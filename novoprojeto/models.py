from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

    
class Situacao(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status            


class Recurso(models.Model):
    tiporecurso = models.CharField(max_length=20)

    def __str__(self):
        return self.tiporecurso



class Novoprojeto(models.Model):
    
    DIFICULDADE_CHOICES = (
        ('D', 'Difícil'),
        ('M', 'Médio'),
        ('F', 'Fácil')
    )
    NOTIFICACOES_CHOICES = (
        ('URGENTE', 'URGENCIA DE ENTREGA'),
        ('REGULAR', 'PRAZO REGULAR'),
        ('ESTÁVEL', 'LONGO PRAZO')
    )

    
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=100)
    escopo = models.TextField()

    dificuldade = models.CharField(max_length=1, choices=DIFICULDADE_CHOICES)

    observacao = models.TextField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    situacao = models.ForeignKey(Situacao, null=True, blank=True, on_delete=models.DO_NOTHING)
    recurso = models.ForeignKey(Recurso, on_delete=models.DO_NOTHING)
    orcamento = models.FloatField(null=True, blank=True)

    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

  
    def __str__(self):
        return self.titulo

    @property
    def css_dificuldade(self):
        if self.dificuldade == 'F':
            return 'projeto-facil'
        elif self.dificuldade == 'M':
            return 'projeto-medio'
        elif self.dificuldade == 'D':
            return 'projeto-dificil'



class Validacao(models.Model): 
    #**trabalhar com a segurança de acessos 
    projeto = models.ForeignKey(Novoprojeto, on_delete=models.DO_NOTHING) 

    executado = models.BooleanField(default=False)  
    aprovado = models.BooleanField(default=False)  
   
    def __str__(self):
        return self.projeto.titulo  






 
class Listagem(models.Model): 

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
        
    descricao_home = models.CharField(max_length=100)


    categoria = models.ManyToManyField(Categoria)
   
    quantidade_projetos = models.IntegerField()

    dificuldade = models.CharField(     
        max_length=1, choices=Novoprojeto.DIFICULDADE_CHOICES
    )

    projetos = models.ManyToManyField(Validacao)
  

    def __str__(self):
        return self.descricao_home 

    categoria = models.ManyToManyField(Categoria) #**na tela passa a categoria

    categoria = models.ManyToManyField(Categoria)
   
    quantidade_projetos = models.IntegerField()

    dificuldade = models.CharField(     
        max_length=1, choices=Novoprojeto.DIFICULDADE_CHOICES
    )

    projetos = models.ManyToManyField(Validacao)
  

    def __str__(self):

        return self.descricao_home ##**nome do ambiente criado 

        return self.descricao_home 

