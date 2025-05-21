from django.contrib import admin
from .models import HscScienceSubjects, HscCommerceSubjects, HscArtsSubjects, HscAdmissionScience, HscAdmissionArts, HscAdmissionCommerce, HscSession, ParentInfo, Address, AcademicInformation, Payment

# Register your models here.
admin.site.register(HscSession)
admin.site.register(HscScienceSubjects)
admin.site.register(HscCommerceSubjects)
admin.site.register(HscArtsSubjects)
admin.site.register(HscAdmissionScience)
admin.site.register(ParentInfo)
admin.site.register(Address)
admin.site.register(AcademicInformation)
admin.site.register(Payment)