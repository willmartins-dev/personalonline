from django.db import models
from django.contrib.auth.models import User
import datetime


class DadosIniciais(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    data_nascimento = models.DateField(blank=True)
    altura = models.IntegerField(blank=True)
    peso = models.FloatField(blank=True)
    genero = models.CharField(max_length=255, blank=True)

    def Idade(self):
        hoje = datetime.date.today()
        idade = hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return idade
    
    def calc_agua(self):
        idade = self.Idade()
        quantidade = self.peso*idade
        return round(quantidade/1000, 2)
    
    def calc_kcal(self):
        peso = self.peso
        altura = self.altura
        idade=self.Idade()
        genero = self.genero

        if genero == 'masculino':
            tmb = 66.47+(13.75*peso)+(5.003*altura)-(6.775*idade)
        elif genero == 'feminino':
            tmb=655.09+(9.563*peso)+(1.85*altura)-(4.676*idade)
        elif not genero:
            tmb = 0

        return round(tmb,2)

class Anamnese(models.Model):
    # Dados pessoais
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Histórico de saúde
    lesoes_anteriores = models.TextField(blank=True, null=True, help_text="Descreva lesões, dores, cirurgias, problemas ortopédicos, etc.")
    doencas_cronicas = models.TextField(blank=True, null=True, help_text="Hipertensão, diabetes, problemas cardíacos, pulmonares, etc.")
    medicamentos = models.TextField(blank=True, null=True, help_text="Liste medicamentos em uso e seus efeitos.")
    alergias = models.TextField(blank=True, null=True, help_text="Alerta sobre alergias conhecidas.")
    restricoes_medicas = models.TextField(blank=True, null=True, help_text="Qualquer restrição ou recomendação médica.")

    # Estilo de vida e hábitos
    atividade_fisica_atual = models.TextField(blank=True, null=True, help_text="Descreva sua prática atual de exercícios.")
    horas_sono_noite = models.PositiveIntegerField(blank=True, null=True)
    fumante = models.BooleanField(default=False)
    cigarros_dia = models.PositiveIntegerField(blank=True, null=True)
    consumo_alcool = models.TextField(blank=True, null=True)
    alimentacao = models.TextField(blank=True, null=True, help_text="Refeições por dia, consumo de água, suplementação.")

    # Objetivos e metas
    objetivos = models.TextField(help_text="Quais são seus principais objetivos com o treino?")
    preferencias_exercicios = models.TextField(blank=True, null=True, help_text="Gosta ou não gosta de alguns exercícios?")

    # Declaração de consentimento
    declaracao_verdade = models.BooleanField(default=False, help_text="Declaro que as informações prestadas são verdadeiras.")

    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    

