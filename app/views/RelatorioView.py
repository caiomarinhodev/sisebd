import datetime
from django.contrib import messages

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q

from app.models import Igreja


def get_filter_relatorio(request):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    visitantes = 0
    tpresentes = 0
    tfaltosos = 0
    arr_presentes = []
    arr_faltosos = []
    arr_datas = []
    initData = request.GET['init_data']
    endData = request.GET['end_data']
    aulas = igreja.aulas.filter(
        Q(data__gt=decrement_day(get_data_formated(initData)),
          data__lt=increment_day(get_data_formated(endData)))
    )
    try:
        for aula in aulas:
            visitantes += int(aula.visitantes)
            tpresentes += len(aula.presentes.all())
            tfaltosos += len(aula.faltosos.all())
            arr_datas.append(aula.data.strftime('%d-%m-%Y'))
            arr_presentes.append(len(aula.presentes.all()))
            arr_faltosos.append(len(aula.faltosos.all()))
        presentes = float(float(tpresentes) / float(len(igreja.alunos.all()))) / len(aulas)
        faltosos = (1 - presentes) * 100
    except ZeroDivisionError:
        for aula in igreja.aulas.all():
            visitantes += int(aula.visitantes)
            tpresentes += len(aula.presentes.all())
            tfaltosos += len(aula.faltosos.all())
            arr_datas.append(aula.data.strftime('%d-%m-%Y'))
            arr_presentes.append(len(aula.presentes.all()))
            arr_faltosos.append(len(aula.faltosos.all()))
        presentes = 0
        faltosos = 0
        messages.error(request, 'Nao foi possivel encontrar aulas registradas neste intervalo de datas.')
    if len(arr_datas) > 8:
        arr_datas = arr_datas[-1:-8]
        arr_faltosos = arr_faltosos[-1:-8]
        arr_presentes = arr_presentes[-1:-8]
    dados = (len(igreja.aulas.all()) + len(igreja.classes.all()) + len(igreja.alunos.all()) + \
             len(igreja.departamentos.all()) + len(igreja.professores.all())) / 4
    return render_to_response('index.html', {'igreja': igreja,
                                             'presentes': round(presentes * 100, 1),
                                             'faltosos': round(faltosos, 1),
                                             'visitantes': visitantes,
                                             'dados': dados,
                                             'initData': initData,
                                             'endData': endData,
                                             'arr_datas': arr_datas,
                                             'arr_presentes': arr_presentes,
                                             'arr_faltosos': arr_faltosos},
                              context_instance=RequestContext(request))


def get_relatorios(request):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    if igreja.primeira_entrada:
        primeira_entrada = 1
        igreja.primeira_entrada = False
        igreja.save()
    else:
        primeira_entrada = 0
    visitantes = 0
    presentes = 0
    faltosos = 0
    tpresentes = 0
    tfaltosos = 0
    arr_datas = []
    arr_presentes = []
    arr_faltosos = []
    try:
        initData = igreja.aulas.first().data.strftime('%d-%m-%Y')
        endData = datetime.datetime.now().strftime('%d-%m-%Y')
    except AttributeError:
        initData = ''
        endData = ''
    try:
        for aula in igreja.aulas.all():
            visitantes += int(aula.visitantes)
            tpresentes += len(aula.presentes.all())
            tfaltosos += len(aula.faltosos.all())
            arr_datas.append(aula.data.strftime('%d-%m-%Y'))
            arr_presentes.append(len(aula.presentes.all()))
            arr_faltosos.append(len(aula.faltosos.all()))
        presentes = float(float(tpresentes) / float(len(igreja.alunos.all()))) / len(igreja.aulas.all())
        faltosos = (1 - presentes) * 100
    except ZeroDivisionError:
        for aula in igreja.aulas.all():
            visitantes += int(aula.visitantes)
            tpresentes += len(aula.presentes.all())
            tfaltosos += len(aula.faltosos.all())
            arr_datas.append(aula.data.strftime('%d-%m-%Y'))
            arr_presentes.append(len(aula.presentes.all()))
            arr_faltosos.append(len(aula.faltosos.all()))
        presentes = 0
        faltosos = 0
    if len(arr_datas) > 8:
        arr_datas = arr_datas[-1:-8]
        arr_faltosos = arr_faltosos[-1:-8]
        arr_presentes = arr_presentes[-1:-8]
    dados = (len(igreja.aulas.all()) + len(igreja.classes.all()) + len(igreja.alunos.all()) + \
             len(igreja.departamentos.all()) + len(igreja.professores.all())) / 4
    return render_to_response('index.html', {'igreja': igreja,
                                             'presentes': round(presentes * 100, 1),
                                             'faltosos': round(faltosos, 1),
                                             'visitantes': visitantes,
                                             'dados': dados,
                                             'initData': initData,
                                             'endData': endData,
                                             'arr_datas': arr_datas,
                                             'arr_presentes': arr_presentes,
                                             'primeira_entrada': primeira_entrada,
                                             'arr_faltosos': arr_faltosos},
                              context_instance=RequestContext(request))


def get_data_formated(data):
    # replace = data.replace('/', '-')
    date = datetime.datetime.strptime(data, '%d/%m/%Y')
    new_d = datetime.datetime.strftime(date, '%Y-%m-%d')
    return new_d


def increment_day(data):
    date_1 = datetime.datetime.strptime(data, '%Y-%m-%d')
    end_date = date_1 + datetime.timedelta(days=1)
    return datetime.datetime.strftime(end_date, '%Y-%m-%d')


def decrement_day(data):
    date_1 = datetime.datetime.strptime(data, '%Y-%m-%d')
    end_date = date_1 - datetime.timedelta(days=1)
    return datetime.datetime.strftime(end_date, '%Y-%m-%d')
