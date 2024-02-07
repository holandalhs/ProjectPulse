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


'''class Notificacao(models.Model):
    notas = models.CharField(max_length=20)

    def __str__(self):
        return self.notas
   ''' 

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

    ##notificacao = models.CharField(max_length=15, choices=NOTIFICACOES_CHOICES, null=True, blank=True)

   

    #**mais a frente, quando a data de finalização for preenchida; o campo 
    #**Situação recebe automaticamente o status de finalizado!

    #**outra funcionalidade: seria gerar alertas na tela inicial para os projetos próximos do vencimento
    #**outra funcionalidade: seria a criação de dashboards para melhor visualização dos projetos

    def __str__(self):
        return self.titulo

