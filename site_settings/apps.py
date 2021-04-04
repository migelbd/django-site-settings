from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SiteSettingsConfig(AppConfig):
    name = 'site_settings'
    verbose_name = _('site settings')

    def ready(self):
        import site_settings.signals