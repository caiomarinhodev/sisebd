from django.contrib import messages
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from app.models import Igreja, Departamento, Classe, Professor


def list_classes(request):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    return render_to_response('classes.html', {'igreja': igreja},
                              context_instance=RequestContext(request))


def add_classe(request):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    if request.method == 'GET':
        return render_to_response('add_classe.html', {'igreja': igreja},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        data = request.POST
        try:
            professor = Professor.objects.get(id=data['id_professor'])
            new_classe = Classe(nome=data['nome'], professor=professor, idade_minima=data['idade_minima'],
                                idade_maxima=data['idade_maxima'])
            new_classe.save()
            depto = Departamento.objects.get(id=data['id_depto'])
            depto.classes.add(new_classe)
            depto.save()
            igreja.classes.add(new_classe)
            igreja.save()
            messages.success(request, 'Classe criada com sucesso.')
            return redirect('/classes')
        except:
            messages.error(request, 'Houve algum erro.')
            return redirect('/add-classe')


def edit_classe(request, id):
    classe = Classe.objects.get(id=id)
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    if request.method == 'GET':
        return render_to_response('edit_classe.html', {'igreja': igreja,
                                                       'classe': classe},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        data = request.POST
        try:
            classe.nome = data['nome']
            classe.idade_minima = data['idade_minima']
            classe.idade_maxima = data['idade_maxima']
            professor = Professor.objects.get(id=data['id_professor'])
            classe.professor = professor
            classe.save()
            deptoAtual = classe.departamento_set.first()
            deptoAtual.classes.remove(classe)
            deptoAtual.save()
            depto = Departamento.objects.get(id=data['id_depto'])
            depto.classes.add(classe)
            depto.save()
            messages.success(request, 'Classe editada com sucesso.')
            return redirect('/classes')
        except:
            messages.error(request, 'Nao foi possivel editar classe.')
            return redirect('/classes')


def view_classe(request, id):
    classe = Classe.objects.get(id=id)
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    if request.method == 'GET':
        return render_to_response('view_classe.html', {'igreja': igreja,
                                                       'classe': classe},
                                  context_instance=RequestContext(request))
    else:
        return redirect('/classes')


def remove_classe(request, id):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    try:
        classe = Classe.objects.get(id=id)
        igreja.classes.remove(classe)
        igreja.save()
        try:
            depto = Departamento.objects.get(id=classe.departamento_set.first().id)
            depto.classes.remove(classe)
            depto.save()
        except:
            pass
        classe.delete()
        messages.success(request, 'Classe removida com sucesso.')
        return redirect('/classes')
    except:
        messages.error(request, 'Nao foi possivel remover classe.')
        return redirect('/classes')