# coding: utf-8

from django.contrib import admin
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from mailauth.models import MailUser

from models import YandexDomain

class YandexDomainAdmin(admin.ModelAdmin):
    list_display = ('name', )
    actions = ('domain_report', )

    def domain_report(self, request, queryset):
        """
        Shows mailboxes present on Yandex, but not registered as MailUsers in mailauth app
        and mailboxes present in mailauth app, but not on Yandex
        """

        result = {}
        for yandex_domain in queryset:
            result[yandex_domain.name] = {}
            api_request_pages = []
            page = 0
            while True:
                api_request_pages.append(yandex_domain.api.get_users_list(page=page)['emails'])
                if api_request_pages[-1]['found'] + page >= api_request_pages[-1]['total']:
                    break
                page += api_request_pages[-1]['found']
            yandex_users = set()
            yandex_users.update(*[map(lambda x: '@'.join((x['name'], yandex_domain.name)).lower(), emails['email'])
                               for emails in api_request_pages])
            local_users = set(map(lambda x: x.lower(), MailUser.objects.filter(external_username__contains="@"+yandex_domain.name)
                                .values_list('external_username', flat=True)))
            result[yandex_domain.name]['missing_from_yandex'] = local_users - yandex_users
            result[yandex_domain.name]['missing_from_local'] = yandex_users - local_users
        return render_to_response('yandexmail/admin/domain_report.html', {'result': result},
            context_instance=RequestContext(request))
    domain_report.short_description = "Generate Yandex/Local difference report"


admin.site.register(YandexDomain, YandexDomainAdmin)