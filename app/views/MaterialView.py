from base64 import b64encode
import datetime
import json

from django.contrib import messages
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
import pyimgur
import requests

from app.models import Igreja, Pessoa, Material


def list_materiais(request):
    igreja = None
    aluno = None
    professor = None
    categoria = int(request.session['categoria'])
    if categoria == 1:
        professor = Pessoa.objects.get(email=request.session['email']).professor_set.first()
    elif categoria == 2:
        aluno = Pessoa.objects.get(email=request.session['email']).aluno_set.first()
    else:
        igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    return render_to_response('materiais.html', {'igreja': igreja,
                                                 'aluno': aluno,
                                                 'professor': professor},
                              context_instance=RequestContext(request))


def add_material(request):
    igreja = None
    aluno = None
    professor = None
    categoria = int(request.session['categoria'])
    if categoria == 1:
        professor = Pessoa.objects.get(email=request.session['email']).professor_set.first()
    elif categoria == 2:
        aluno = Pessoa.objects.get(email=request.session['email']).aluno_set.first()
    else:
        igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    if request.method == 'GET':
        return render_to_response('add_material.html', {'igreja': igreja,
                                                        'aluno': aluno,
                                                        'professor': professor},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        data = request.POST
        file = ''
        if data['categoria'] == 'Imagem':
            CLIENT_ID = "cdadf801dc167ab"
            data = b64encode(request.FILES['file'].read())
            client = pyimgur.Imgur(CLIENT_ID)
            r = client._send_request('https://api.imgur.com/3/image', method='POST', params={'image': data})
            file = r['link']
        else:
            url = "https://content.dropboxapi.com/2/files/upload"
            name = "/" + str(request.FILES['file'].name)
            headers = {
                "Authorization": "Bearer M6iN1nYzh_YAAAAAAACHm34PsRKmgPWvVI6uSALYMTqZxGUcopC4pr7K7OkfFfaZ",
                "Content-Type": "application/octet-stream",
                "Dropbox-API-Arg": "{\"path\":\"" + name + "\"}"
            }
            data = b64encode(request.FILES['file'].read())
            r = requests.post(url, headers=headers, data=data)
            # print r.json()
            if r.status_code == 200 or r.status_code == 201:
                url = "https://api.dropboxapi.com/2/sharing/create_shared_link"
                headers = {
                    "Authorization": "Bearer M6iN1nYzh_YAAAAAAACHmqe-TsJhb-Dur_EB09HNKaguknUwnq2a_PprLOwiSS3W",
                    "Content-Type": "application/json"
                }
                data = {
                    "path": "/Apps/pagseguroarquivos" + name,
                    "short_url": False
                }
                # print json.dumps(data)
                r = requests.post(url, headers=headers, data=json.dumps(data))
                file = r.json()['url']
        try:
            if categoria == 0:
                autor = None
            else:
                autor = Pessoa.objects.get(email=request.session['email'])

            new_material = Material(titulo=request.POST['titulo'], descricao=request.POST['descricao'],
                                    file=file, categoria=request.POST['categoria'], autor=autor)
            new_material.save()
            if categoria == 1:
                professor = Pessoa.objects.get(email=request.session['email']).professor_set.first()
                igreja = professor.igreja_set.first()
                igreja.materiais.add(new_material)
                igreja.save()
                classe = professor.classe_set.first()
                classe.materiais.add(new_material)
                classe.save()
                messages.success(request, 'Material adicionado com sucesso.')
                return redirect('/materiais')
            elif categoria == 2:
                aluno = Pessoa.objects.get(email=request.session['email']).aluno_set.first()
                igreja = aluno.igreja_set.first()
                igreja.materiais.add(new_material)
                igreja.save()
                classe = aluno.classe_set.first()
                classe.materiais.add(new_material)
                classe.save()
                messages.success(request, 'Material adicionado com sucesso.')
                return redirect('/materiais')
            else:
                igreja = Igreja.objects.get(email_responsavel=request.session['email'])
                igreja.materiais.add(new_material)
                igreja.save()
                messages.success(request, 'Material adicionado com sucesso.')
                return redirect('/materiais')
        except:
            messages.error(request, 'Houve algum erro.')
            return redirect('/add-material')


def remove_material(request, id):
    igreja = None
    aluno = None
    professor = None
    categoria = int(request.session['categoria'])
    try:
        material = Material.objects.get(id=id)
        if categoria == 1:
            professor = Pessoa.objects.get(email=request.session['email']).professor_set.first()
            igreja = professor.igreja_set.first()
            igreja.materiais.remove(material)
            igreja.save()
        elif categoria == 2:
            aluno = Pessoa.objects.get(email=request.session['email']).aluno_set.first()
            igreja = aluno.igreja_set.first()
            igreja.materiais.remove(material)
            igreja.save()
        else:
            igreja = Igreja.objects.get(email_responsavel=request.session['email'])
            igreja.materiais.remove(material)
            igreja.save()
            try:
                classe = material.classe_set.first()
                classe.materiais.remove(material)
                classe.save()
            except:
                pass
        material.delete()
        messages.success(request, 'Material removido com sucesso.')
        return redirect('/materiais')
    except:
        messages.error(request, 'Nao foi possivel remover o material.')
        return redirect('/materiais')


def get_data_formated(data):
    # replace = data.replace('/', '-')
    date = datetime.datetime.strptime(data, '%d/%m/%Y')
    new_d = datetime.datetime.strftime(date, '%Y-%m-%d')
    return new_d
