import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext

from app.models import Igreja


def get_relatorios(request):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    visitantes = 0
    presentes = 0
    faltosos = 0
    tpresentes = 0
    tfaltosos = 0
    for aula in igreja.aulas.all():
        visitantes += int(aula.visitantes)
        tpresentes += len(aula.presentes.all())
        tfaltosos += len(aula.faltosos.all())
    presentes = float(float(tpresentes) / float(len(igreja.alunos.all()))) / len(igreja.aulas.all())
    faltosos = (1 - presentes) * 100
    dados = (len(igreja.aulas.all()) + len(igreja.classes.all()) + len(igreja.alunos.all()) + \
            len(igreja.departamentos.all()) + len(igreja.professores.all()))/4
    return render_to_response('relatorios.html', {'igreja': igreja,
                                                  'presentes': round(presentes * 100, 1),
                                                  'faltosos': round(faltosos, 1),
                                                  'visitantes': visitantes,
                                                  'dados': dados},
                              context_instance=RequestContext(request))


def get_data_formated(data):
    # replace = data.replace('/', '-')
    date = datetime.datetime.strptime(data, '%d/%m/%Y')
    new_d = datetime.datetime.strftime(date, '%Y-%m-%d')
    return new_d
