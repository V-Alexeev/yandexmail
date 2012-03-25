from django.db.models.signals import post_save
from django.dispatch import receiver

from nginxmailauth.models import MailUser
from nginxmailauth.utils import generate_password

from models import YandexDomain


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
    yd.api.create_user(username, password)
    instance.external_password = password
    instance.save()