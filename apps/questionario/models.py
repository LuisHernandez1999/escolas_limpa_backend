from django.db import models
from apps.escola.models import Escola

class Questionario_coleta_escolar(models.Model):
    prefixo_caminhao = models.CharField(max_length=50)
    data = models.DateField()
    bairro = models.CharField(max_length=100)
    
    motorista_nome = models.CharField(max_length=100)
    motorista_matricula = models.CharField(max_length=50)
    
    coletor_nome = models.CharField(max_length=100)
    coletor_matricula = models.CharField(max_length=50)
    
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='coletas')
    
    horario_chegada = models.TimeField()
    horario_saida = models.TimeField()
    
    
    bag_plastico = models.PositiveIntegerField(default=0)
    bag_papel = models.PositiveIntegerField(default=0)
    bag_aluminio = models.PositiveIntegerField(default=0)
    bag_eletronico = models.PositiveIntegerField(default=0)

    # Quantidade de avaliação
    bag_vazio = models.PositiveIntegerField(default=0)
    bag_semi_cheio = models.PositiveIntegerField(default=0)
    bag_cheio = models.PositiveIntegerField(default=0)
    
    assinatura_responsavel = models.CharField(max_length=200)
    telefone_responsavel = models.CharField(max_length=20)
    cpf_responsavel = models.CharField(max_length=14)  # Formato XXX.XXX.XXX-XX

    def calcular_pontos(self):
        pontos = (
            self.bag_plastico +
            self.bag_papel +
            self.bag_aluminio +
            self.bag_eletronico +
            self.bag_vazio +
            self.bag_semi_cheio +
            self.bag_cheio
        )
        return pontos

    def __str__(self):
        return f"Coleta {self.prefixo_caminhao} - {self.data} - {self.bairro}"
