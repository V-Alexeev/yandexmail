from django.core.management.base import BaseCommand

from mailauth.models import MailUser
from mailauth.utils import generate_password

from yandexmail.models import YandexDomain
from yandexmail.YandexMailApi import YandexMailApi, YandexApiException


class Command(BaseCommand):
    args = ''
    help = 'Sets random passwords for all Yandex accounts'

    def handle(self, *args, **options):
        for yandex_domain in YandexDomain.objects.all():
            for user in MailUser.objects.filter(external_username__contains="@"+yandex_domain.name):
                username, domain = user.external_username.split('@')
                new_password = generate_password()
                try:
                    yandex_domain.api.edit_user_details(login=username, password=new_password)
                except YandexApiException, e:
                    self.stderr.write("Failed to set new password for %s, the error was: %s" % (user.external_username, e.message))
                else:
                    user.external_password = new_password
                    user.save()