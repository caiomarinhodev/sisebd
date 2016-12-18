from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render_to_response
from django.template import RequestContext


# Render LoginInit
from app.views import RelatorioView


def logout(request):
    request.session.clear()
    return redirect('/login')


def presentation(request):
    return render_to_response('presentation.html', context_instance=RequestContext(request))


@login_required(login_url='/admin/login/')
def home(request):
    return RelatorioView.get_relatorios(request)
