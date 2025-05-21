from django.contrib import admin
from .models import HscScienceSubjects, HscCommerceSubjects, HscArtsSubjects, HscAdmissionScience, HscAdmissionArts, HscAdmissionCommerce, HscSession

# Register your models here.
admin.site.register(HscSession)
admin.site.register(HscScienceSubjects)
admin.site.register(HscCommerceSubjects)
admin.site.register(HscArtsSubjects)
admin.site.register(HscAdmissionScience)