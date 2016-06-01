import json

from django.shortcuts import redirect
from django.views.generic.base import TemplateView
import requests


class LoginView(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context


class WhoView(TemplateView):
    template_name = "login_part2.html"

    def get_context_data(self, **kwargs):
        context = super(WhoView, self).get_context_data(**kwargs)
        return context


class RegisterView(TemplateView):
    template_name = "login_igreja.html"

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        return context


class ConfirmView(TemplateView):
    template_name = "login_pessoa.html"

    def get_context_data(self, **kwargs):
        context = super(ConfirmView, self).get_context_data(**kwargs)
        return context


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
    nome = user_info['given_name']
    sobrenome = user_info['family_name']
    foto = user_info['picture']
    print user_info
    if user_info['identities'][0]['connection'] == 'google-oauth2':
        email = user_info['email']
    elif user_info['identities'][0]['connection'] == 'windowslive':
        email = user_info['email']
    elif user_info['identities'][0]['connection'] == 'auth0':
        email = user_info['email']

    # try:
    #     obj = Usuario.objects.get(login=login)
    #     usuario = obj
    #     request.session['id'] = usuario.id
    # except:
    #     usuario = Usuario(login=login, senha=senha, nome=nome, sobrenome=sobrenome, nacionalidade=nacionalidade,
    #                       nivel_colaborador=colaborador, foto=foto, email=email, link=link)
    #     usuario.save()
    #     request.session['id'] = usuario.id
    return redirect('/who')


    # send_mail('Pedido de Cliente', mess_pedido,
    #               'postmaster@sandbox3cb2aeaee26e40d99701d79339faccce.mailgun.org',
    #               ['sac.dcher@gmail.com', 'caiodotdev@gmail.com'], fail_silently=False)

    # def get_data_formated(data):
    #     # replace = data.replace('/', '-')
    #     date = datetime.datetime.strptime(data, '%d/%m/%Y')
    #     new_d = datetime.datetime.strftime(date, '%Y-%m-%d')
    #     return new_d
