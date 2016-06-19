from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from app.models import Igreja, Aula, Pessoa


def list_diarios(request):
    igreja=None
    aluno=None
    professor=None
    categoria = int(request.session['categoria'])
    if categoria == 1:
        professor = Pessoa.objects.get(email=request.session['email']).professor_set.first()
    elif categoria == 2:
        aluno = Pessoa.objects.get(email=request.session['email']).aluno_set.first()
    else:
        igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    return render_to_response('diarios.html', {'igreja': igreja,
                                               'aluno': aluno,
                                               'professor': professor},
                              context_instance=RequestContext(request))


def view_diario(request, id):
    aula = Aula.objects.get(id=id)
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    if request.method == 'GET':
        return render_to_response('view_diario.html', {'igreja': igreja,
                                                       'aula': aula},
                                  context_instance=RequestContext(request))
    else:
        return redirect('/diarios')
