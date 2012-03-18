from django.db import models

from YandexMailApi import YandexMailApi


class YandexDomain(models.Model):
    name = models.CharField('Domain name', max_length=200, db_index=True, unique=True)
    api_token = models.CharField('Yandex API token', max_length=200,
                help_text="You can get it at https://pddimp.yandex.ru/get_token.xml?domain_name=example.com")

    @property
    def api(self):
        return YandexMailApi(self.api_token)