from django.db import models
from django.utils.translation import gettext_lazy as _


def get_bool_value(value) -> bool:
    try:
        return bool(int(value))
    except ValueError:
        return True


class SettingBase(models.Model):
    alias = models.CharField(max_length=256, verbose_name=_('alias'), unique=True, db_index=True)
    name = models.CharField(max_length=256, verbose_name=_('name'))
    cache_time = models.IntegerField(default=0, verbose_name=_('cache time'),
                                     help_text=_('cache time in seconds (specify 0 to not cache)'))

    load_in_template = models.BooleanField(default=False, verbose_name=_('load in template'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))

    class Meta:
        abstract = True

    @property
    def cache_key(self) -> str:
        return f'setting_{self.pk}'


class SettingGroup(SettingBase):

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')


class Setting(SettingBase):
    group = models.ForeignKey(SettingGroup, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('group'))
    value = models.TextField(verbose_name=_('value'))

    value_type = models.PositiveSmallIntegerField(choices=(
        (1, _('Integer')),
        (2, _('String')),
        (3, _('Boolean')),
    ), default=2, verbose_name=_('type of value'))

    class Meta:
        verbose_name = _('setting')
        verbose_name_plural = _('settings')

    def clear_cache(self):
        from django.core.cache import cache
        cache.remove(self.cache_key)

    def get_value(self):
        return Setting.get_value_by_type(self.value, self.value_type)

    @classmethod
    def get_value_by_type(cls, value, value_type):
        if value_type == 1:
            return int(value)
        if value_type == 2:
            return value
        if value_type == 3:
            return get_bool_value(value)

    def __str__(self):
        return f'{self.alias}'
