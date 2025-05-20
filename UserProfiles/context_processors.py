from .models import SiteSettings

def institution_info(request):
    settings = SiteSettings.objects.first()
    return {
        'site_settings': settings
    }
