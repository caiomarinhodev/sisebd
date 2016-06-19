from base64 import b64encode
import datetime

from django.contrib import messages
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
import pyimgur

from app.models import Igreja, Classe, Pessoa, Professor


def get_configuracoes(request):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    return render_to_response('config.html', {'igreja': igreja},
                              context_instance=RequestContext(request))


def edit_configuracoes(request):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    data = request.POST
    try:
        igreja.nome_igreja = data['nome_igreja']
        igreja.nome_responsavel = data['nome_responsavel']
        igreja.qtd_membros = data['qtd_membros']
        igreja.plano = data['plano']
        igreja.telefone = data['telefone']
        CLIENT_ID = "cdadf801dc167ab"
        data = b64encode(request.FILES['imagem'].read())
        client = pyimgur.Imgur(CLIENT_ID)
        r = client._send_request('https://api.imgur.com/3/image', method='POST', params={'image': data})
        igreja.foto = r['link']
        igreja.save()
        messages.success(request, 'Alteracoes realizadas com sucesso.')
        return redirect('/config')
    except:
        messages.error(request, 'Houve algum erro.')
        return redirect('/config')
