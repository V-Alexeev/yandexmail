from django.core.management.base import BaseCommand

from mailauth.models import MailUser

from yandexmail.models import YandexDomain
from yandexmail.YandexMailApi import YandexApiException

class Command(BaseCommand):
    args = ''
    help = 'Sets passwords for all Yandex accounts according to the values in local db'

    def handle(self, *args, **options):
        for yandex_domain in YandexDomain.objects.all():
            for user in MailUser.objects.filter(external_username__contains="@"+yandex_domain.name):
                username, domain = user.external_username.split('@')
                try:
                    yandex_domain.api.edit_user_details(login=username, password=user.external_password)
                except YandexApiException, e:
                    self.stderr.write("Failed to set password for %s, the error was: %s" % (user.external_username, e.message))
                    