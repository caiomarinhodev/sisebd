import datetime
from django.contrib import messages

from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from app.models import Igreja, Classe, Aluno, Aula


def list_aulas(request):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    return render_to_response('aulas.html', {'igreja': igreja},
                              context_instance=RequestContext(request))


def get_add_aula(request):
    data = request.POST
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    try:
        classe = Classe.objects.get(id=data['id_classe'])
        return render_to_response('add_aula.html', {'igreja': igreja,
                                                    'classe': classe},
                                  context_instance=RequestContext(request))
    except:
        return redirect('/aulas')


def post_add_aula(request, id):
    data = request.POST
    classe = Classe.objects.get(id=id)
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    try:
        presentes_arr = data.getlist('presentes')
        new_aula = Aula(data=get_data_formated(data['data']),
                        ofertas=data['ofertas'], biblias=data['biblias'],
                        revistas=data['revistas'], visitantes=data['visitantes'])
        new_aula.save()
        print presentes_arr
        for p_id in presentes_arr:
            al = Aluno.objects.get(id=p_id)
            new_aula.presentes.add(al)
        for fal in classe.alunos.all():
            if str(fal.id) not in presentes_arr:
                new_aula.faltosos.add(fal)
        new_aula.save()
        classe.aulas.add(new_aula)
        classe.save()
        igreja.aulas.add(new_aula)
        igreja.save()
        messages.success(request, 'Aula criada com sucesso.')
        return redirect('/aulas')
    except:
        messages.error(request, 'Houve algum erro.')
        return redirect('/add-aula')


def remove_aula(request, id):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    try:
        aula = Aula.objects.get(id=id)
        igreja.aulas.remove(aula)
        try:
            classe = Classe.objects.get(id=aula.classe_set.first().id)
            classe.aulas.remove(aula)
            classe.save()
        except:
            pass
        aula.delete()
        messages.success(request, 'Aula removida com sucesso.')
        return redirect('/aulas')
    except:
        messages.error(request, 'Nao foi possivel remover aula.')
        return redirect('/aulas')


def get_data_formated(data):
    # replace = data.replace('/', '-')
    date = datetime.datetime.strptime(data, '%d/%m/%Y')
    new_d = datetime.datetime.strftime(date, '%Y-%m-%d')
    return new_d
