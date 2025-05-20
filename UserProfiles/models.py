from django.db import models

# Create your models here.
class SiteSettings(models.Model):
    favicon = models.ImageField(upload_to='favicon/', blank=True, null=True)
    institution_name = models.CharField(max_length=255)
    institution_description = models.CharField(max_length=255, blank=True, null=True)
    footer = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    address = models.TextField()
    mobile_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

class Notice(models.Model):
    notice_title = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    notice_description = models.TextField(blank=True, null=True)
    notice_file = models.FileField(upload_to='notices/', blank=True, null=True)
    # date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notice_title

    class Meta:
        verbose_name = "Notice"
        verbose_name_plural = "Notices"