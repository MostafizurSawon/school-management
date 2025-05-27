from django.contrib import admin
from .models import  HscCommerceSubjects, HscArtsSubjects, HscAdmissionScience, HscAdmissionArts, HscAdmissionCommerce, HscSession, ParentInfo, Address, AcademicInformation, Payment, SscSession, HscScienceCompulsorySubjects, HscScienceOptionalSubjects, HscScienceMainSubjects, HscScienceFourthSubjects, HscFeeType

# Register your models here.
admin.site.register(HscSession)
admin.site.register(SscSession)
# admin.site.register(HscScienceSubjects)
admin.site.register(HscCommerceSubjects)
admin.site.register(HscArtsSubjects)
admin.site.register(HscAdmissionScience)
admin.site.register(ParentInfo)
admin.site.register(Address)
admin.site.register(AcademicInformation)
admin.site.register(Payment)
admin.site.register(HscFeeType)

admin.site.register(HscScienceCompulsorySubjects)
admin.site.register(HscScienceOptionalSubjects)
admin.site.register(HscScienceMainSubjects)
admin.site.register(HscScienceFourthSubjects)