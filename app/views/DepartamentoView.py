from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from app.models import Igreja, Departamento


def list_departamentos(request):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    return render_to_response('departamentos.html', {'igreja': igreja},
                       context_instance=RequestContext(request))


def add_departamento(request):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    if request.method == 'GET':
        return render_to_response('add_departamento.html', {'igreja': igreja},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        data = request.POST
        try:
            new_depto = Departamento(descricao=data['descricao'])
            new_depto.save()
            igreja.departamentos.add(new_depto)
            igreja.save()
            return redirect('/departamentos')
        except:
            return redirect('/add-depto')


def edit_departamento(request, id):
    depto = Departamento.objects.get(id=id)
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    if request.method == 'GET':
        return render_to_response('edit_departamento.html', {'igreja': igreja,
                                                             'depto': depto},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        data = request.POST
        try:
            depto.descricao = data['descricao']
            depto.save()
            return redirect('/departamentos')
        except:
            return redirect('/departamentos')


def view_departamento(request, id):
    depto = Departamento.objects.get(id=id)
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    if request.method == 'GET':
        return render_to_response('view_departamento.html', {'igreja': igreja,
                                                             'depto': depto},
                                  context_instance=RequestContext(request))
    else:
        return redirect('/departamentos')
