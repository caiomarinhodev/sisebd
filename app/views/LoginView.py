import json
from django.contrib import messages

from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
import requests

from app.models import Pessoa, Professor, Aluno, Igreja, Departamento, Classe


# Render LoginInit
from app.views import RelatorioView


def get_login(request):
    return render_to_response('login.html', context_instance=RequestContext(request))


# Quem esta logando?
def get_who(request):
    if request.method == 'GET':
        return render_to_response('login_part2.html', context_instance=RequestContext(request))
    elif request.method == 'POST':
        data = request.POST
        categoria = data['categoria']
        request.session['categoria'] = categoria
        return redirect('/')


# Renderiza e recebe POST da tela de registro de igrejas
def get_register(request):
    if request.method == 'GET':
        nome = request.session['nome']
        email = request.session['email']
        return render_to_response('registro_igreja.html', {'nome': nome, 'email': email},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        data = request.POST
        nome_igreja = data['nome_igreja']
        telefone = data['telefone']
        qtd_membros = data['qtd_membros']
        nova_igreja = Igreja(nome_responsavel=request.session['nome'], email_responsavel=request.session['email'],
                             telefone=telefone, nome_igreja=nome_igreja, qtd_membros=qtd_membros,
                             foto=request.session['foto'])
        nova_igreja.save()
        return redirect('/')


# Gerencia quem esta logando para onde vai!
def loga(request, categoria):
    if int(categoria) == 1:
        if 'logado' in request.session:
            if int(request.session['logado']) == 1:
                return RelatorioView.get_relatorios(request)
        else:
            try:
                return render_to_response('confirm_pessoa.html', {'igrejas': Igreja.objects.all()},
                                          context_instance=RequestContext(request))
            except:
                request.session.clear()
                messages.error(request, 'Usuario nao existe.')
                return redirect('/login')
    elif int(categoria) == 2:
        if 'logado' in request.session:
            if int(request.session['logado']) == 1:
                return RelatorioView.get_relatorios(request)
        else:
            try:
                return render_to_response('confirm_pessoa.html', {'igrejas': Igreja.objects.all()},
                                          context_instance=RequestContext(request))
            except:
                request.session.clear()
                messages.error(request, 'Usuario nao existe.')
                return redirect('/login')
    else:
        try:
            return RelatorioView.get_relatorios(request)
        except Igreja.DoesNotExist:
            return redirect('/register')


def verifica_sessao(request):
    if 'email' in request.session:
        if 'categoria' in request.session:
            if request.session['email'] and request.session['categoria']:
                return loga(request, categoria=request.session['categoria'])
        else:
            return redirect('/who')
    else:
        return redirect('/login')


def callback_handling(request):
    code = request.GET.get('code')

    json_header = {'content-type': 'application/json'}

    token_url = "https://{domain}/oauth/token".format(domain='sisebd.auth0.com')

    token_payload = {
        'client_id': 'mArhMhxXWjMaqVaDLrfbCgP2VmiDlt24',
        'client_secret': '3gBmAUpjQZGM8PRzGSJcYJt_ylY3eE_39EK10JaV5IqQPp-EIdWR6qLTqGkaakEe',
        'redirect_uri': 'http://localhost:8000/callback',
        'code': code,
        'grant_type': 'authorization_code'
    }

    token_info = requests.post(token_url, data=json.dumps(token_payload), headers=json_header).json()

    user_url = "https://{domain}/userinfo?access_token={access_token}" \
        .format(domain='sisebd.auth0.com', access_token=token_info['access_token'])

    user_info = requests.get(user_url).json()
    nome = user_info['name']
    foto = user_info['picture']
    if user_info['identities'][0]['connection'] == 'google-oauth2':
        email = user_info['email']
    elif user_info['identities'][0]['connection'] == 'auth0':
        email = user_info['email']
    else:
        email = user_info['email']
    request.session['email'] = email
    request.session['nome'] = nome
    request.session['foto'] = foto
    return redirect('/who')


def confirma_pessoa(request):
    data = request.POST
    categoria = int(request.session['categoria'])
    email = request.session['email']
    try:
        pessoa = Pessoa.objects.get(email=email)
        pessoa.nome = request.session['nome']
        pessoa.save()
    except Pessoa.DoesNotExist:
        request.session.clear()
        messages.error(request, 'Usuario nao cadastrado.')
        return redirect('/login')
    except Pessoa.MultipleObjectsReturned:
        request.session.clear()
        messages.error(request, 'Usuario nao cadastrado.')
        return redirect('/login')
    if categoria == 1:
        professor = pessoa.professor_set.first()
        professor.foto = request.session['foto']
        professor.save()
        if professor.habilitado and int(professor.igreja_set.first().id) == int(data['id_igreja']):
            try:
                request.session['logado'] = 1
                return RelatorioView.get_relatorios(request)
            except:
                request.session.clear()
                messages.error(request, 'Nao foi possivel renderizar o sistema.')
                return redirect('/login')
        else:
            messages.error(request, 'Este usuario nao esta habilitado a acessar o sistema.')
            return redirect('/login')
    else:
        aluno = pessoa.aluno_set.first()
        aluno.foto = request.session['foto']
        aluno.save()
        if aluno.habilitado and int(aluno.igreja_set.first().id) == int(data['id_igreja']):
            try:
                request.session['logado'] = 1
                return RelatorioView.get_relatorios(request)
            except Aluno.DoesNotExist:
                request.session.clear()
                messages.error(request, 'Nao foi possivel renderizar o sistema..')
                return redirect('/login')
        else:
            messages.error(request, 'Este usuario nao esta habilitado a acessar o sistema.')
            return redirect('/login')


def logout(request):
    request.session.clear()
    return redirect('/login')
