

def settings(request):
    from site_settings.helper import get_context_settings

    return dict(
        settings=get_context_settings()
    )
