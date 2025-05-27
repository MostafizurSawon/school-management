from django.contrib import admin
from .models import (
     SscSession, HscFeeType,
    
    # Science
    HscAdmissionScience, ParentInfo, Address, AcademicInformation, Payment,
    HscScienceCompulsorySubjects, HscScienceOptionalSubjects, HscScienceMainSubjects, HscScienceFourthSubjects,
    
    # Arts
    HscAdmissionArts, ParentInfoArts, AddressArts, AcademicInformationArts, PaymentArts,
    HscArtsCompulsorySubjects, HscArtsOptionalSubjects, HscArtsMainSubjects, HscArtsFourthSubjects,
    
    # Commerce
    HscAdmissionCommerce, ParentInfoCommerce, AddressCommerce, AcademicInformationCommerce, PaymentCommerce,
    HscCommerceCompulsorySubjects, HscCommerceOptionalSubjects, HscCommerceMainSubjects, HscCommerceFourthSubjects, HscSessionForPayment, ProgramType, Program, FeePurpose, FeeStructure
)

# Core Models
# @admin.register(HscSession)
# class HscSessionAdmin(admin.ModelAdmin):
#     list_display = ('session', 'fee')
#     search_fields = ('session',)

@admin.register(SscSession)
class SscSessionAdmin(admin.ModelAdmin):
    list_display = ('session',)
    search_fields = ('session',)

@admin.register(HscFeeType)
class HscFeeTypeAdmin(admin.ModelAdmin):
    list_display = ('fee_type', 'amount')
    search_fields = ('fee_type',)

# === Science Admin ===
@admin.register(HscAdmissionScience)
class HscAdmissionScienceAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_roll', 'ssc_roll', 'hsc_session', 'mobile', 'gender')
    search_fields = ('name', 'ssc_roll', 'class_roll', 'mobile')
    list_filter = ('hsc_session', 'gender', 'blood_group')

@admin.register(ParentInfo)
class ParentInfoAdmin(admin.ModelAdmin):
    list_display = ('student', 'fathers_name_english', 'mother_name_english', 'guardian')
    search_fields = ('student__name', 'fathers_name_english', 'mother_name_english')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('student', 'district', 'postal_code', 'permanent_address_same')
    search_fields = ('student__name', 'district', 'policeStation')

@admin.register(AcademicInformation)
class AcademicInformationAdmin(admin.ModelAdmin):
    list_display = ('student', 'ssc_board', 'ssc_year', 'sscGpa')
    search_fields = ('student__name', 'ssc_board', 'ssc_year')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'method', 'amount', 'status', 'payment_date')
    search_fields = ('student__name', 'transaction_id', 'receipt_number')
    list_filter = ('status', 'method')

admin.site.register(HscScienceCompulsorySubjects)
admin.site.register(HscScienceOptionalSubjects)
admin.site.register(HscScienceMainSubjects)
admin.site.register(HscScienceFourthSubjects)

# === Arts Admin ===
@admin.register(HscAdmissionArts)
class HscAdmissionArtsAdmin(HscAdmissionScienceAdmin): pass

@admin.register(ParentInfoArts)
class ParentInfoArtsAdmin(ParentInfoAdmin): pass

@admin.register(AddressArts)
class AddressArtsAdmin(AddressAdmin): pass

@admin.register(AcademicInformationArts)
class AcademicInformationArtsAdmin(AcademicInformationAdmin): pass

@admin.register(PaymentArts)
class PaymentArtsAdmin(PaymentAdmin): pass

admin.site.register(HscArtsCompulsorySubjects)
admin.site.register(HscArtsOptionalSubjects)
admin.site.register(HscArtsMainSubjects)
admin.site.register(HscArtsFourthSubjects)

# === Commerce Admin ===
@admin.register(HscAdmissionCommerce)
class HscAdmissionCommerceAdmin(HscAdmissionScienceAdmin): pass

@admin.register(ParentInfoCommerce)
class ParentInfoCommerceAdmin(ParentInfoAdmin): pass

@admin.register(AddressCommerce)
class AddressCommerceAdmin(AddressAdmin): pass

@admin.register(AcademicInformationCommerce)
class AcademicInformationCommerceAdmin(AcademicInformationAdmin): pass

@admin.register(PaymentCommerce)
class PaymentCommerceAdmin(PaymentAdmin): pass

admin.site.register(HscCommerceCompulsorySubjects)
admin.site.register(HscCommerceOptionalSubjects)
admin.site.register(HscCommerceMainSubjects)
admin.site.register(HscCommerceFourthSubjects)



admin.site.register(HscSessionForPayment)
admin.site.register(ProgramType)
admin.site.register(Program)
admin.site.register(FeePurpose)
admin.site.register(FeeStructure)

