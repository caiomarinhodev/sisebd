from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from app.models import Igreja, Aula


def list_diarios(request):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    return render_to_response('diarios.html', {'igreja': igreja},
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
