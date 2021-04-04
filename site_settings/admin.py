from django.contrib import admin
from site_settings import models
from django.utils.translation import gettext_lazy as _


def clear_cache(self, request, qs):
    self.message_user(request, 'OK')


clear_cache.short_description = _('Clear cache')
clear_cache.allowed_permissions = ('change',)


@admin.register(models.SettingGroup)
class SettingGroupAdmin(admin.ModelAdmin):
    actions = [clear_cache]

    list_display = (
        'id',
        'alias',
        'name',
        'cache_time',
        'created_at',
        'updated_at',
    )
    list_display_links = (
        'id',
        'alias',
    )

    date_hierarchy = 'created_at'

    search_fields = (
        'alias',
        'name',
    )


@admin.register(models.Setting)
class SettingAdmin(admin.ModelAdmin):
    actions = [clear_cache]
    list_display = (
        'id',
        'alias',
        'name',
        'cache_time',
        'group',
        'value',
        'created_at',
    )
    list_display_links = (
        'id',
        'alias',
    )

    date_hierarchy = 'created_at'

    search_fields = (
        'alias',
        'name',
        'group__name',
    )

    list_filter = (
        'group',
    )