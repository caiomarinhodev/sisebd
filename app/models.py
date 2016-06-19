from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Pessoa(models.Model):
    """
        Modelo Pessoa
    """
    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=50, blank=True, null=True)
    nome_pai = models.CharField(max_length=100, blank=True, null=True)
    nome_mae = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    estado_civil = models.CharField(max_length=100, blank=True, null=True)
    idade = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefone_residencial = models.CharField(max_length=30, blank=True, null=True)
    telefone_comercial = models.CharField(max_length=30, blank=True, null=True)
    telefone_celular = models.CharField(max_length=30, blank=True, null=True)
    status = models.BooleanField(default=True, blank=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=30, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nome).upper() + " - " + str(self.email)


class Aluno(models.Model):
    """
        Modelo Aluno
    """
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    foto = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    primeira_entrada = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pessoa.nome).upper()


class Professor(models.Model):
    """
        Modelo Professor
    """
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    foto = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    primeira_entrada = models.BooleanField(default=True)
    habilitado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pessoa.nome).upper()


class Aula(models.Model):
    """
        Modelo Professor
    """
    data = models.DateField()
    ofertas = models.CharField(max_length=10)
    biblias = models.CharField(max_length=10)
    revistas = models.CharField(max_length=10)
    visitantes = models.CharField(max_length=10)
    presentes = models.ManyToManyField(Aluno, related_name='%(class)s_presentes', blank=True)
    faltosos = models.ManyToManyField(Aluno, related_name='%(class)s_faltosos', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.data).upper()


# Create your models here.

class Material(models.Model):
    file = models.FileField()
    titulo = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    autor = models.ForeignKey(Pessoa, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Classe(models.Model):
    """
        Modelo Classe
    """
    alunos = models.ManyToManyField(Aluno, blank=True)
    aulas = models.ManyToManyField(Aula, blank=True)
    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, blank=True)
    materiais = models.ManyToManyField(Material, blank=True)
    idade_minima = models.CharField(max_length=10)
    idade_maxima = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nome).upper()


class Departamento(models.Model):
    """
        Modelo Departamento
    """
    descricao = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    classes = models.ManyToManyField(Classe, blank=True)
    professores = models.ManyToManyField(Professor, blank=True)

    def __str__(self):
        return str(self.descricao).upper()


class Igreja(models.Model):
    """
        Modelo Igreja
    """
    nome_responsavel = models.CharField(max_length=100)
    email_responsavel = models.EmailField()
    telefone = models.CharField(max_length=50, blank=True, null=True)
    nome_igreja = models.CharField(max_length=100)
    qtd_membros = models.CharField(max_length=10, blank=True, null=True)
    foto = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    classes = models.ManyToManyField(Classe, blank=True)
    departamentos = models.ManyToManyField(Departamento, blank=True)
    professores = models.ManyToManyField(Professor, blank=True)
    alunos = models.ManyToManyField(Aluno, blank=True)
    aulas = models.ManyToManyField(Aula, blank=True)
    materiais = models.ManyToManyField(Material, blank=True)
    primeira_entrada = models.BooleanField(default=True)
    plano = models.CharField(max_length=100, default='GRATUITO')

    def __str__(self):
        return str(self.nome_igreja).upper()
