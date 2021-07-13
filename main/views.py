from django.shortcuts import render
from django.views.generic import TemplateView


def my_view(request):
    return render(request, 'main/layout.html', {})


class HomeView(TemplateView):

    template_name = 'main/base.html'
