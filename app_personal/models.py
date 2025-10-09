from django.db import models
from django.contrib.auth.models import User


class CategoriaExercicios(models.Model):
    titulo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    url = models.TextField(null=True)

    def __str__(self):
        return self.titulo
    
class Exercicios(models.Model):
    categoria = models.ForeignKey(CategoriaExercicios, on_delete=models.CASCADE)
    exercicio = models.CharField(max_length=255)
    url = models.TextField()

    def __str__(self):
        return self.exercicio
    
class Mesociclo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    periodizacao = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)
    duracao = models.DateField(null=True)

    def __str__(self):
        return self.titulo
class Microciclo(models.Model):
    mesociclo = models.ForeignKey(Mesociclo, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)

class ExerciciosCliente(models.Model):
    microciclo = models.ForeignKey(Microciclo, on_delete=models.CASCADE)
    exercicio = models.CharField(max_length=255)
    url_img = models.TextField(blank=True)
    series = models.CharField(max_length=255)
    reps = models.CharField(max_length=255)
    obs = models.CharField(max_length=255)
    conjugado = models.IntegerField(null=True)


