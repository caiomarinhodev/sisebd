from django.contrib import admin

from app.models import *


class AlunoInline(admin.TabularInline):
    model = Aluno


class ClasseInline(admin.TabularInline):
    model = Classe


class AulaInline(admin.TabularInline):
    model = Aula


class ContaInline(admin.TabularInline):
    model = Conta


class DepartamentoInline(admin.TabularInline):
    model = Departamento


class IgrejaAdmin(admin.ModelAdmin):
    """
        Modelo Igreja Admin
    """
    inlines = [DepartamentoInline, ClasseInline, AlunoInline, AulaInline, ContaInline, ]
    list_display = (
        'nome_igreja', 'email_responsavel', 'telefone', 'qtd_membros', 'created_at', 'updated_at', 'habilitado')


class DepartamentoAdmin(admin.ModelAdmin):
    """
        Modelo Departamento Admin
    """
    list_display = ('nome', 'igreja', 'created_at', 'updated_at',)


class ClasseAdmin(admin.ModelAdmin):
    """
        Modelo Classe Admin
    """
    list_display = ('nome', 'professor', 'igreja', 'created_at', 'updated_at',)


class AlunoAdmin(admin.ModelAdmin):
    """
        Modelo Pessoa Admin
    """
    list_display = ('nome', 'igreja', 'classe', 'sexo', 'idade', 'cidade', 'estado')
    list_filter = ('igreja', 'classe',)


class ContaAdmin(admin.ModelAdmin):
    """
        Modelo Aluno Admin
    """
    list_display = ('igreja', 'user', 'tipo', 'primeira_entrada', 'created_at', 'updated_at',)


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'descricao', 'created_at', 'updated_at',)


class AulaAdmin(admin.ModelAdmin):
    """
        Modelo Professor Admin
    """
    list_display = ('classe', 'igreja', 'data', 'created_at',)


admin.site.register(Aula, AulaAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Classe, ClasseAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Igreja, IgrejaAdmin)
admin.site.register(Material)
admin.site.register(Conta, ContaAdmin)
