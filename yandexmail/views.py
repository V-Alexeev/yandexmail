from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from mailauth.models import MailUser

from models import YandexDomain


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    def clean(self):
        try:
            mail_user = MailUser.objects.select_related().get(internal_username=self.cleaned_data['username'])
        except (MailUser.DoesNotExist, MailUser.MultipleObjectsReturned):
            raise forms.ValidationError("Incorrect username or password")

        if mail_user.authenticate(self.cleaned_data['password']):
            self.cleaned_data['user'] = mail_user
        else:
            raise forms.ValidationError("Incorrect username or password")

        return self.cleaned_data


def webmail_login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            mail_user = form.cleaned_data['user']
            username, domain = mail_user.external_username.split('@')
            yd = YandexDomain.objects.get(name=domain)
            redirect_url = yd.api.get_auth_url(domain, username)
            return HttpResponseRedirect(redirect_url)
    else:
        form = LoginForm()
    return render_to_response('yandexmail/main.html', {'form': form},
                               context_instance=RequestContext(request))