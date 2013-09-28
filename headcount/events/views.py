from django.http import HttpResponse
from django.views.generic import View

from braces.views import LoginRequiredMixin


class Dashboard(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("HOLA")
