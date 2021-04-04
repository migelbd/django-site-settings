import functools
import typing
from collections import defaultdict
from django.core.cache import cache

from site_settings.models import Setting

VALUES_TYPE_MAP = (
    (int, 1),
    (str, 2),
    (bool, 3),
)

CACHE_SETTINGS_KEY = 'settings_%s'


def cached_setting(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        is_force = kwargs.pop('force', False)
        key = CACHE_SETTINGS_KEY % args[0]
        if key in cache and not is_force:
            return cache.get(key)
        result, cache_time = func(*args, **kwargs)
        cache.set(key, result, timeout=cache_time)
        return result

    return wrapper


@cached_setting
def get_setting(alias: str, default: typing.Optional[typing.Union[str, int, bool]] = None, get_or_create: bool = False):
    if get_or_create:
        assert default, 'default must be set'
        instance, _ = Setting.objects.values('value', 'value_type').get_or_create(
            alias=alias,
            defaults=dict(
                alias=alias,
                value=str(default),
                value_type=dict(VALUES_TYPE_MAP).get(type(default))
            )
        )
        return Setting.get_value_by_type(instance['value'], instance['value_type'])

    try:
        instance = Setting.objects.values('value', 'value_type').get(alias=alias)
        return Setting.get_value_by_type(instance['value'], instance['value_type'])
    except Setting.DoesNotExist:
        return default


@cached_setting
def get_setting_group(alias: str):
    instances = Setting.objects.filter(group__alias=alias)
    return {instance.alias: instance.get_value() for instance in instances}


def get_context_settings():
    result = defaultdict(dict)
    settings_values = Setting.objects.values('alias', 'value', 'value_type').filter(load_in_template=True)
    settings_values_group = Setting.objects.values('alias', 'value', 'value_type', 'group__alias').filter(
        group__load_in_template=True)
    for item in settings_values_group:
        grp = item['group__alias']
        result[grp][item['alias']] = Setting.get_value_by_type(item['value'], item['value_type'])
    settings = {instance['alias']: Setting.get_value_by_type(instance['value'], instance['value_type']) for instance in
                settings_values}

    result.update(settings)
    return dict(result)
