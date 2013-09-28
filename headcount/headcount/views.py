from django.core.urlresolvers import reverse_lazy
from django.views import generic

from authtools import views as auth_views
from braces.views import LoginRequiredMixin, FormValidMessageMixin

from . import forms


class CustomLogoutView(LoginRequiredMixin, auth_views.LogoutView):
    url = reverse_lazy('events:home')


class CustomLoginView(auth_views.LoginView):
    form_class = forms.HeadcountAuthenticationForm
    success_url = reverse_lazy('events:home')


class RegisterView(FormValidMessageMixin, generic.FormView):
    form_class = forms.HeadcountUserCreationForm
    form_valid_message = 'Your account has been created!'
    success_url = reverse_lazy('accounts:login')
    template_name = "registration/register.html"
