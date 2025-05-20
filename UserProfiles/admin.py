from django.contrib import admin
from django.utils.html import mark_safe
from .models import SiteSettings

# Register your models here.

class SiteSettingsAdmin(admin.ModelAdmin):
    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" height="50" />')
        return "-"
    logo_preview.short_description = "Logo"

    list_display = ['institution_name', 'logo_preview', 'mobile_number']

admin.site.register(SiteSettings, SiteSettingsAdmin)
