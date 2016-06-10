import datetime
from django.contrib import messages

from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from app.models import Igreja, Classe, Aluno, Pessoa


def list_alunos(request):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    return render_to_response('alunos.html', {'igreja': igreja},
                              context_instance=RequestContext(request))


def add_aluno(request):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    if request.method == 'GET':
        return render_to_response('add_aluno.html', {'igreja': igreja},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        data = request.POST
        try:
            new_pessoa = Pessoa(nome=data['nome'], sexo=data['sexo'], nome_pai=data['nome_pai'],
                                nome_mae=data['nome_mae'],
                                data_nascimento=get_data_formated(data['data_nascimento']),
                                estado_civil=data['estado_civil'],
                                idade=data['idade'], email=data['email'],
                                telefone_residencial=data['telefone_residencial'],
                                telefone_comercial=data['telefone_comercial'],
                                telefone_celular=data['telefone_celular'],
                                endereco=data['endereco'], numero=data['numero'],
                                bairro=data['bairro'], cidade=data['cidade'], cep=data['cep'], estado=data['estado'])
            new_pessoa.save()
            new_aluno = Aluno(pessoa=new_pessoa)
            new_aluno.foto = 'http://lorempixel.com/128/128/'
            new_aluno.save()
            classe = Classe.objects.get(id=data['id_classe'])
            classe.alunos.add(new_aluno)
            classe.save()
            igreja.alunos.add(new_aluno)
            igreja.save()
            messages.success(request, 'Aluno criado com sucesso.')
            return redirect('/alunos')
        except:
            messages.error(request, 'Erro ao criar aluno.')
            return redirect('/add-aluno')


def edit_aluno(request, id):
    pessoa = Pessoa.objects.get(id=id)
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    if request.method == 'GET':
        return render_to_response('edit_aluno.html', {'igreja': igreja,
                                                      'pessoa': pessoa},
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        data = request.POST
        try:
            pessoa.nome = data['nome']
            pessoa.sexo = data['sexo']
            pessoa.nome_pai = data['nome_pai']
            pessoa.nome_mae = data['nome_mae']
            pessoa.estado_civil = data['estado_civil']
            pessoa.idade = data['idade']
            pessoa.email = data['email']
            pessoa.telefone_residencial = data['telefone_residencial']
            pessoa.telefone_celular = data['telefone_celular']
            pessoa.telefone_comercial = data['telefone_comercial']
            pessoa.endereco = data['endereco']
            pessoa.numero = data['numero']
            pessoa.bairro = data['bairro']
            pessoa.cidade = data['cidade']
            pessoa.cep = data['cep']
            pessoa.estado = data['estado']
            pessoa.save()
            messages.success(request, 'Aluno editado com sucesso.')
            return redirect('/alunos')
        except:
            messages.error(request, 'Houve algum erro.')
            return redirect('/alunos')


def view_aluno(request, id):
    pessoa = Pessoa.objects.get(id=id)
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    try:
        aulas = pessoa.aluno_set.all()[0].classe_set.all()[0].aulas.all()
        presencas = (len(aulas.filter(presentes__id__exact=pessoa.aluno_set.all()[0].id))*100)/len(aulas)
        faltas = 100 - presencas

        if request.method == 'GET':
            return render_to_response('view_aluno.html', {'igreja': igreja,
                                                          'pessoa': pessoa,
                                                          'aulas': len(aulas),
                                                          'presencas': presencas,
                                                          'faltas':faltas},
                                      context_instance=RequestContext(request))
        else:
            messages.error(request, 'Nao foi possivel ver aluno.')
            return redirect('/alunos')
    except:
        messages.error(request, 'Houve algum erro.')
        return redirect('/alunos')


def remove_aluno(request, id):
    igreja = Igreja.objects.get(email_responsavel=request.session['email'])
    try:
        aluno = Aluno.objects.get(id=id)
        igreja.alunos.remove(aluno)
        classe = Classe.objects.get(id=aluno.classe_set.all()[0].id)
        classe.alunos.remove(aluno)
        aluno.delete()
        messages.success(request, 'Aluno deletado com sucesso.')
        return redirect('/alunos')
    except:
        messages.error(request, 'Nao foi possivel remover aluno.')
        return redirect('/alunos')


def get_data_formated(data):
    # replace = data.replace('/', '-')
    date = datetime.datetime.strptime(data, '%d/%m/%Y')
    new_d = datetime.datetime.strftime(date, '%Y-%m-%d')
    return new_d
