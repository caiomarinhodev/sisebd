from django.contrib import admin

from app.models import *


class IgrejaAdmin(admin.ModelAdmin):
    """
        Modelo Igreja Admin
    """
    list_display = ('nome_igreja', 'nome_responsavel', 'email_responsavel', 'created_at', 'updated_at',)
    list_filter = ('nome_igreja', 'email_responsavel',)


class DepartamentoAdmin(admin.ModelAdmin):
    """
        Modelo Departamento Admin
    """
    list_display = ('descricao', 'created_at', 'updated_at',)


class ClasseAdmin(admin.ModelAdmin):
    """
        Modelo Classe Admin
    """
    list_display = ('nome', 'created_at', 'updated_at',)
    list_filter = ('nome',)


class PessoaAdmin(admin.ModelAdmin):
    """
        Modelo Pessoa Admin
    """
    list_display = ('nome', 'email', 'status',)
    list_filter = ('nome',)


class AlunoAdmin(admin.ModelAdmin):
    """
        Modelo Aluno Admin
    """
    list_display = ('pessoa', 'created_at', 'updated_at',)


class ProfessorAdmin(admin.ModelAdmin):
    """
        Modelo Professor Admin
    """
    list_display = ('pessoa', 'created_at', 'updated_at',)


class AulaAdmin(admin.ModelAdmin):
    """
        Modelo Professor Admin
    """
    list_display = ('data', 'created_at',)


admin.site.register(Aula, AulaAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Classe, ClasseAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Igreja, IgrejaAdmin)
