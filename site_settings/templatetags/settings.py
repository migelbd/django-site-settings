from django import template
from site_settings.helper import get_setting, get_setting_group

register = template.Library()


@register.simple_tag(name='setting')
def get_setting_tag(alias, default=None):
    return get_setting(alias, default)


@register.simple_tag(name='setting_group')
def get_setting_group_tag(alias):
    return get_setting_group(alias)