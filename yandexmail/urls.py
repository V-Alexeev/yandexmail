from django.conf.urls.defaults import patterns, url
from views import webmail_login

urlpatterns = patterns('',
    url(r'$', webmail_login, name='yandexmail_webmail_login'),
)
