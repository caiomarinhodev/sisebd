"""djangoboiler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from app import views
import app.views.LoginView
import app.views.DepartamentoView
import app.views.ClasseView
import app.views.AlunoView
import app.views.ProfessorView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/login/$', auth_views.login),
    url(r'^$', views.LoginView.verifica_sessao, name='index'),
    url(r'^login', views.LoginView.get_login, name='login'),
    url(r'^callback', views.LoginView.callback_handling, name='callback'),
    url(r'^who', views.LoginView.get_who, name='who'),
    url(r'^register', views.LoginView.get_register, name='register'),
    url(r'^logout', views.LoginView.logout, name='logout'),
    url(r'^add-depto', views.DepartamentoView.add_departamento, name='add-depto'),
    url(r'^departamentos/', views.DepartamentoView.list_departamentos, name='departamentos'),
    url(r'^edit-depto/(?P<id>\d+)', views.DepartamentoView.edit_departamento, name='edit-depto'),
    url(r'^view-depto/(?P<id>\d+)', views.DepartamentoView.view_departamento, name='view-depto'),
    url(r'^add-classe', views.ClasseView.add_classe, name='add-classe'),
    url(r'^classes/', views.ClasseView.list_classes, name='classes'),
    url(r'^edit-classe/(?P<id>\d+)', views.ClasseView.edit_classe, name='edit-classe'),
    url(r'^view-classe/(?P<id>\d+)', views.ClasseView.view_classe, name='view-classe'),
    url(r'^add-aluno', views.AlunoView.add_aluno, name='add-aluno'),
    url(r'^alunos/', views.AlunoView.list_alunos, name='alunos'),
    url(r'^edit-aluno/(?P<id>\d+)', views.AlunoView.edit_aluno, name='edit-aluno'),
    url(r'^view-aluno/(?P<id>\d+)', views.AlunoView.view_aluno, name='view-aluno'),
    url(r'^add-professor', views.ProfessorView.add_professor, name='add-professor'),
    url(r'^professores/', views.ProfessorView.list_professores, name='professores'),
    url(r'^edit-professor/(?P<id>\d+)', views.ProfessorView.edit_professor, name='edit-professor'),
    url(r'^view-professor/(?P<id>\d+)', views.ProfessorView.view_professor, name='view-professor'),
]
