from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from app.models import Igreja, Departamento
from django.contrib import messages


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
            messages.success(request, 'Departamento criado com sucesso.')
            return redirect('/departamentos')
        except:
            messages.error(request, 'Nao foi possivel criar o departamento')
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
            messages.success(request, 'Departamento editado com sucesso.')
            return redirect('/departamentos')
        except:
            messages.error(request, 'Houve algum erro.')
            return redirect('/departamentos')


def view_departamento(request, id):
    depto = Departamento.objects.get(id=id)
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    if request.method == 'GET':
        return render_to_response('view_departamento.html', {'igreja': igreja,
                                                             'depto': depto},
                                  context_instance=RequestContext(request))
    else:
        messages.error(request, 'Houve algum erro.')
        return redirect('/departamentos')


def remove_departamento(request, id):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    try:
        depto = Departamento.objects.get(id=id)
        igreja.departamentos.remove(depto)
        igreja.save()
        depto.delete()
        messages.success(request, 'Departamento deletado com sucesso.')
        return redirect('/departamentos')
    except:
        return redirect('/departamentos')
