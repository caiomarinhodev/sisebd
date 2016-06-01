from django.shortcuts import redirect
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = "test.html"

    def get(self, request, *args, **kwargs):
        if request.session['email'] is None:
            redirect('/login')

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context
