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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/login/$', auth_views.login),
    url(r'^$', views.LoginView.verifica_sessao, name='index'),
    url(r'^login', views.LoginView.get_login, name='login'),
    url(r'^callback', views.LoginView.callback_handling, name='callback'),
    url(r'^who', views.LoginView.get_who, name='who'),
    url(r'^register', views.LoginView.get_register, name='register'),
    url(r'^logout', views.LoginView.logout, name='logout'),
]
