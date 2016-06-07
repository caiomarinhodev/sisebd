import datetime

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
        for p_id in presentes_arr:
            al = Aluno.objects.get(id=p_id)
            new_aula.presentes.add(al)
        for fal in classe.alunos.all():
            if str(fal.id) not in presentes_arr:
                new_aula.faltosos.add(al)
        new_aula.save()
        classe.aulas.add(new_aula)
        classe.save()
        igreja.aulas.add(new_aula)
        igreja.save()
        return redirect('/aulas')
    except:
        return redirect('/add-aula')


def remove_aula(request, id):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    try:
        aula = Aula.objects.get(id=id)
        igreja.aulas.remove(aula)
        id_classe = aula.classe_set.all()
        classe = Classe.objects.get(id=id_classe[0].id)
        aula.delete()
        return redirect('/aulas')
    except:
        return redirect('/aulas')


def get_data_formated(data):
    # replace = data.replace('/', '-')
    date = datetime.datetime.strptime(data, '%d/%m/%Y')
    new_d = datetime.datetime.strftime(date, '%Y-%m-%d')
    return new_d
