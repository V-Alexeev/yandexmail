from django.db.models.signals import post_save
from django.dispatch import receiver

from nginxmailauth.models import MailUser
from nginxmailauth.utils import generate_password

from models import YandexDomain
from YandexMailApi import YandexApiException


@receiver(post_save, sender=MailUser)
def create_user_at_yandex(sender, **kwargs):
    if not kwargs['created']:
        return
    instance = kwargs['instance']
    try:
        username, domain = instance.external_username.split('@')
    except ValueError:
        return
    try:
        yd = YandexDomain.objects.get(name=domain)
    except YandexDomain.DoesNotExist:
        return
    password = generate_password()
    try:
        yd.api.create_user(username, password)
    except YandexApiException:
        pass
    else:
        instance.external_password = password
        instance.save()