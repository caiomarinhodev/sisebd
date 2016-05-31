from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Igreja(models.Model):
    """
        Modelo Igreja
    """
    nome_responsavel = models.CharField(max_length=100)
    email_responsavel = models.EmailField()
    telefone = models.CharField(max_length=50, blank=True, null=True)
    nome_igreja = models.CharField(max_length=100)
    qtd_membros = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nome_igreja).upper()


class Departamento(models.Model):
    """
        Modelo Departamento
    """
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.descricao).upper()


class Classe(models.Model):
    """
        Modelo Classe
    """
    nome = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    idade_minima = models.IntegerField()
    idade_maxima = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nome).upper()


class Pessoa(models.Model):
    """
        Modelo Pessoa
    """
    EMPTY = ''
    MASC = 'Masculino'
    FEM = 'Feminino'
    SOLTEIRO = 'Solteiro(a)'
    CASADO = 'Casado(a)'
    DIVORCIADO = 'Divorciado(a)'
    VIUVO = 'Viuvo(a)'

    TIPOS = (
        (EMPTY, ''),
        (MASC, 'Masculino'),
        (FEM, 'Feminino'),
    )

    CIVIL = (
        (EMPTY, ''),
        (SOLTEIRO, 'Solteiro(a)'),
        (CASADO, 'Casado(a)'),
        (VIUVO, 'Viuvo(a)'),
        (DIVORCIADO, 'Divorciado(a)'),
    )
    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=50, choices=TIPOS, blank=True, null=True)
    nome_pai = models.CharField(max_length=100, blank=True, null=True)
    nome_mae = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    estado_civil = models.CharField(max_length=100, blank=True, null=True, choices=CIVIL)
    idade = models.IntegerField(blank=True, null=True)
    email = models.EmailField()
    telefone_residencial = models.CharField(max_length=30, blank=True, null=True)
    telefone_comercial = models.CharField(max_length=30, blank=True, null=True)
    telefone_celular = models.CharField(max_length=30, blank=True, null=True)
    status = models.BooleanField(default=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=30, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.nome).upper() + " - " + str(self.email)


class Aluno(models.Model):
    """
        Modelo Aluno
    """
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pessoa.nome).upper()

        # from django.forms import inlineformset_factory
        # BookFormSet = inlineformset_factory(Author, Book, fields=('title',))
        # author = Author.objects.get(name='Mike Royko')
        # formset = BookFormSet(instance=author)
