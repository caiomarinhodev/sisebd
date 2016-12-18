from django.contrib import admin

from app.models import *


class DeptoInline(admin.TabularInline):
    model = Igreja.departamentos.through


class ProfessorInline(admin.TabularInline):
    model = Igreja.professores.through


class AulaInline(admin.TabularInline):
    model = Igreja.aulas.through


class MaterialInline(admin.TabularInline):
    model = Igreja.materiais.through


class ClasseInline(admin.TabularInline):
    model = Igreja.classes.through


class AlunoInline(admin.TabularInline):
    model = Igreja.alunos.through


class IgrejaAdmin(admin.ModelAdmin):
    """
        Modelo Igreja Admin
    """
    exclude = ('classes', 'departamentos', 'professores', 'alunos', 'aulas', 'materiais')
    list_display = ('nome_igreja', 'nome_responsavel', 'email_responsavel', 'created_at', 'updated_at',)
    inlines = [DeptoInline, ClasseInline, ProfessorInline, AlunoInline, AulaInline, MaterialInline, ]
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
