from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Pessoa(models.Model):
    """
        Modelo Pessoa
    """

    class Meta:
        abstract = True

    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=50, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    idade = models.CharField(max_length=10, blank=True, null=True)
    telefone_residencial = models.CharField(max_length=30, blank=True, null=True)
    telefone_celular = models.CharField(max_length=30, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=30, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.id) + " - " + str(self.nome).upper() + " - " + str(self.email)

    def __unicode__(self):
        return u'%s' % (str(self.id) + " - " + str(self.nome).upper() + " - " + str(self.email))


class Igreja(TimeStamped, Pessoa):
    """
        Modelo Igreja
    """
    email_responsavel = models.EmailField()
    telefone = models.CharField(max_length=50, blank=True, null=True)
    nome_igreja = models.CharField(max_length=100, unique=True)
    qtd_membros = models.CharField(max_length=10, blank=True, null=True)
    foto = models.URLField(blank=True, null=True)
    habilitado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nome_igreja).upper()

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.nome_igreja)


TIPO_CONTA = (
    ('PROFESSOR', 'PROFESSOR'),
    ('GERENTE', 'GERENTE')
)


class Conta(TimeStamped, Pessoa):
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=TIPO_CONTA)
    foto = models.URLField()
    primeira_entrada = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.user.username)


class Departamento(TimeStamped):
    """
        Modelo Departamento
    """
    nome = models.CharField(max_length=100, null=True, blank=True)
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.nome)


class Classe(TimeStamped):
    """
        Modelo Classe
    """
    nome = models.CharField(max_length=100)
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE)
    professor = models.ForeignKey(Conta, blank=True, null=True)
    materiais = models.ManyToManyField(Material, blank=True)
    idade_minima = models.CharField(max_length=10)
    idade_maxima = models.CharField(max_length=10)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.nome)


class Material(TimeStamped):
    file = models.FileField()
    titulo = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.file)


class Aluno(TimeStamped, Pessoa):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.nome)


class Aula(TimeStamped):
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
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    igreja = models.ForeignKey(Igreja, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.data).upper()

    def __unicode__(self):
        return u'%s' % (self.data)
