from django.db.models.signals import post_save
from django.dispatch import receiver
from site_settings.models import Setting


@receiver(post_save, sender=Setting)
def clear_cache_setting(sender, instance, **kwargs):
    if isinstance(instance, Setting) and instance.cache_time > 0:
        instance.clear_cache()
