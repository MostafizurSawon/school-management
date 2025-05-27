from django.db import models
from django.core.validators import RegexValidator

numeric_validator = RegexValidator(r'^\d{11}$', 'Enter a valid 11-digit number.')

class HscFeeType(models.Model):
    fee_type = models.CharField(max_length=50, unique=True)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.fee_type} - {self.amount} BDT"
    


class HscSession(models.Model):
    session = models.CharField(max_length=9, unique=True)
    fee = models.ForeignKey(HscFeeType, on_delete=models.CASCADE, related_name='hsc_sessions_fee', null=True, blank=True)

    def __str__(self):
        return f"{self.session}"

# class HscSession(models.Model):
#     session = models.CharField(max_length=9, unique=True)
#     program_type = models.CharField(max_length=20, null=True, blank=True)
#     program = models.CharField(max_length=20, null=True, blank=True)
#     fee = models.ForeignKey(HscFeeType, on_delete=models.CASCADE, related_name='hsc_sessions_payment_fee', null=True, blank=True)

#     def __str__(self):
#         return f"{self.session} - {self.program_type} ({self.program}) - {self.fee if self.fee else 'No Fee'}"




class HscSessionForPayment(models.Model):
    session = models.CharField(max_length=20, unique=True)  # e.g., 2021-2022

    def __str__(self):
        return self.session

class ProgramType(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., HSC, Degree, Honours

    def __str__(self):
        return self.name

class Program(models.Model):
    program_type = models.ForeignKey(ProgramType, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=50)  # e.g., Science, Arts, Commerce, Physics

    class Meta:
        unique_together = ('program_type', 'name')

    def __str__(self):
        return f"{self.name} ({self.program_type.name})"

class FeePurpose(models.Model):
    purpose_name = models.CharField(max_length=50, unique=True)  # e.g., Admission Fee, Yearly Fee, Exam Fee

    def __str__(self):
        return self.purpose_name

class FeeStructure(models.Model):
    hsc_session = models.ForeignKey(HscSessionForPayment, on_delete=models.CASCADE, related_name='fees')
    program_type = models.ForeignKey(ProgramType, on_delete=models.CASCADE, related_name='fees')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='fees')
    fee_purpose = models.ForeignKey(FeePurpose, on_delete=models.CASCADE, related_name='fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('hsc_session', 'program_type', 'program', 'fee_purpose')

    def __str__(self):
        return f"{self.hsc_session} | {self.program_type} | {self.program} | {self.fee_purpose} | {self.amount} BDT"



    
class SscSession(models.Model):
    session = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return self.session


# Science Section 

class HscScienceCompulsorySubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class HscScienceOptionalSubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class HscScienceMainSubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class HscScienceFourthSubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class HscAdmissionScience(models.Model):
    program = models.CharField(max_length=20, default='HSC', editable=False)
    type = models.CharField(max_length=10, default='Science', editable=False)
    ssc_roll = models.IntegerField(unique=True)
    hsc_session = models.ForeignKey(HscSessionForPayment, on_delete=models.CASCADE)
    class_roll = models.IntegerField(unique=True)
    merit_position = models.IntegerField()
    name = models.CharField(max_length=100)
    name_bangla = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=11, validators=[numeric_validator])
    blood_group = models.CharField(max_length=3, choices=[
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ])
    birth_certificate_no = models.CharField(max_length=50)
    birthdate = models.DateField()
    marital_status = models.CharField(max_length=10, choices=[
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
    ])
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ])
    nationality = models.CharField(max_length=50)
    religion = models.CharField(max_length=20, choices=[
        ('Islam', 'Islam'),
        ('Hindu', 'Hindu'),
        ('Christian', 'Christian'),
        ('Buddhist', 'Buddhist'),
        ('Other', 'Other'),
    ])
    photo = models.ImageField(upload_to='hsc-science/')

    def __str__(self):
        return f"Name: {self.name} | Group: Science | Class Roll: {self.class_roll} | Session: {self.hsc_session.session}"


class ParentInfo(models.Model):
    student = models.OneToOneField(HscAdmissionScience, on_delete=models.CASCADE, related_name='parent_info')
    fathers_name_english = models.CharField(max_length=100)
    fathers_nid = models.CharField(max_length=17, unique=True)
    fathers_date_of_birth = models.DateField()
    fathers_mobile = models.CharField(max_length=11, validators=[numeric_validator])
    father_occupation = models.CharField(max_length=50)
    fathers_monthly_income = models.IntegerField()
    mother_name_english = models.CharField(max_length=100)
    mothers_nid = models.CharField(max_length=17, unique=True)
    mothers_date_of_birth = models.DateField()
    mothers_mobile = models.CharField(max_length=11, validators=[numeric_validator])
    mother_occupation = models.CharField(max_length=50, blank=True)
    mothers_monthly_income = models.IntegerField()
    guardian = models.CharField(max_length=10, choices=[
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Other', 'Other'),
    ])
    
    guardian_name_english = models.CharField(max_length=100, null=True, blank=True)
    guardian_date_of_birth = models.DateField(null=True, blank=True)
    guardian_mobile = models.CharField(max_length=11, validators=[numeric_validator], null=True, blank=True)
    guardian_nid = models.CharField(max_length=17, unique=True, null=True, blank=True)

    def __str__(self):
        return f"Parents of {self.student.name}"

class Address(models.Model):
    student = models.OneToOneField(HscAdmissionScience, on_delete=models.CASCADE, related_name='address')
    wardNo = models.IntegerField(null=True, blank=True)
    postOffice = models.CharField(max_length=50, null=True, blank=True)
    policeStation = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.IntegerField()
    permanent_address_same = models.BooleanField(default=False)
    permanent_wardNo = models.IntegerField(null=True, blank=True)
    permanent_postOffice = models.CharField(max_length=50, null=True, blank=True)
    permanent_policeStation = models.CharField(max_length=50, null=True, blank=True)
    permanent_district = models.CharField(max_length=50, null=True, blank=True)
    permanent_postal_code = models.IntegerField(null=True, blank=True)
    
    qouta_freedom = models.BooleanField(default=False)
    qouta_community = models.BooleanField(default=False)

    def __str__(self):
        return f"Address of {self.student.name}"

class AcademicInformation(models.Model):
    student = models.OneToOneField(HscAdmissionScience, on_delete=models.CASCADE, related_name='academic_info')
    ssc_board = models.CharField(max_length=20, choices=[
        ('Dhaka', 'Dhaka'),
        ('Rajshahi', 'Rajshahi'),
        ('Comilla', 'Comilla'),
        ('Chittagong', 'Chittagong'),
        ('Barisal', 'Barisal'),
        ('Dinajpur', 'Dinajpur'),
        ('Jessore', 'Jessore'),
        ('Mymensingh', 'Mymensingh'),
        ('Khulna', 'Khulna'),
        ('Sylhet', 'Sylhet'),
        ('Madrasah', 'Madrasah'),
        ('Technical', 'Technical'),
        ('Others', 'Others'),
    ])
    ssc_year = models.CharField(max_length=4, choices=[
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
        ('2028', '2028'),
        ('2029', '2029'),
    ])
    sscInstitution = models.CharField(max_length=100, null=True, blank=True)
    sscRoll = models.IntegerField(null=True, blank=True)
    sscReg = models.IntegerField(null=True, blank=True)
    ssc_session = models.ForeignKey(SscSession, on_delete=models.SET_NULL, null=True, blank=True, related_name='academic_infos_ssc_session_science')

    sscGpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    compulsorySubjects = models.ManyToManyField(HscScienceCompulsorySubjects, related_name='academic_infos_compulsory')
    optionalSubjects = models.ManyToManyField(HscScienceOptionalSubjects, related_name='academic_infos_optional')
    mainSubjects = models.ForeignKey(HscScienceMainSubjects, on_delete=models.SET_NULL, null=True, blank=True, related_name='academic_infos_main')
    FourSubjects = models.ForeignKey(HscScienceFourthSubjects, on_delete=models.SET_NULL, null=True, blank=True, related_name='academic_infos_four')

    def __str__(self):
        return f"Academic Info of {self.student.name}"




class Payment(models.Model):
    student = models.OneToOneField(HscAdmissionScience, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=20, choices=[
        ('Cash', 'Cash'),
        ('Bkash', 'Bkash'),
        ('Nagad', 'Nagad'),
        ('Rocket', 'Rocket'),
    ], null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ], default='Pending')
    receipt_number = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return f"Payment for {self.student.name} - {self.amount} BDT"



# Arts section 

class HscArtsCompulsorySubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class HscArtsOptionalSubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class HscArtsMainSubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class HscArtsFourthSubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"
    

class HscAdmissionArts(models.Model):
    program = models.CharField(max_length=20, default='HSC', editable=False)
    type = models.CharField(max_length=10, default='Humanities', editable=False)
    ssc_roll = models.IntegerField(unique=True)
    hsc_session = models.ForeignKey(HscSession, on_delete=models.CASCADE)
    class_roll = models.IntegerField(unique=True)
    merit_position = models.IntegerField()
    name = models.CharField(max_length=100)
    name_bangla = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=11, validators=[numeric_validator])
    blood_group = models.CharField(max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
    ])
    birth_certificate_no = models.CharField(max_length=50)
    birthdate = models.DateField()
    marital_status = models.CharField(max_length=10, choices=[
        ('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'),
    ])
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'),
    ])
    nationality = models.CharField(max_length=50)
    religion = models.CharField(max_length=20, choices=[
        ('Islam', 'Islam'), ('Hindu', 'Hindu'), ('Christian', 'Christian'),
        ('Buddhist', 'Buddhist'), ('Other', 'Other'),
    ])
    photo = models.ImageField(upload_to='hsc-arts/')

    def __str__(self):
        return f"Name: {self.name} | Group: Arts | Class Roll: {self.class_roll} | Session: {self.hsc_session.session}"
    

class ParentInfoArts(models.Model):
    student = models.OneToOneField(HscAdmissionArts, on_delete=models.CASCADE, related_name='parent_info_arts')
    fathers_name_english = models.CharField(max_length=100)
    fathers_nid = models.CharField(max_length=17, unique=True)
    fathers_date_of_birth = models.DateField()
    fathers_mobile = models.CharField(max_length=11, validators=[numeric_validator])
    father_occupation = models.CharField(max_length=50)
    fathers_monthly_income = models.IntegerField()
    mother_name_english = models.CharField(max_length=100)
    mothers_nid = models.CharField(max_length=17, unique=True)
    mothers_date_of_birth = models.DateField()
    mothers_mobile = models.CharField(max_length=11, validators=[numeric_validator])
    mother_occupation = models.CharField(max_length=50, blank=True)
    mothers_monthly_income = models.IntegerField()
    guardian = models.CharField(max_length=10, choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Other', 'Other')])
    guardian_name_english = models.CharField(max_length=100, null=True, blank=True)
    guardian_date_of_birth = models.DateField(null=True, blank=True)
    guardian_mobile = models.CharField(max_length=11, validators=[numeric_validator], null=True, blank=True)
    guardian_nid = models.CharField(max_length=17, unique=True, null=True, blank=True)

    def __str__(self):
        return f"Parents of {self.student.name}"


class AddressArts(models.Model):
    student = models.OneToOneField(HscAdmissionArts, on_delete=models.CASCADE, related_name='address_arts')
    wardNo = models.IntegerField(null=True, blank=True)
    postOffice = models.CharField(max_length=50, null=True, blank=True)
    policeStation = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.IntegerField()
    permanent_address_same = models.BooleanField(default=False)
    permanent_wardNo = models.IntegerField(null=True, blank=True)
    permanent_postOffice = models.CharField(max_length=50, null=True, blank=True)
    permanent_policeStation = models.CharField(max_length=50, null=True, blank=True)
    permanent_district = models.CharField(max_length=50, null=True, blank=True)
    permanent_postal_code = models.IntegerField(null=True, blank=True)
    qouta_freedom = models.BooleanField(default=False)
    qouta_community = models.BooleanField(default=False)

    def __str__(self):
        return f"Address of {self.student.name}"


class AcademicInformationArts(models.Model):
    student = models.OneToOneField(HscAdmissionArts, on_delete=models.CASCADE, related_name='academic_info_arts')
    ssc_board = models.CharField(max_length=20, choices=[
        ('Dhaka', 'Dhaka'),
        ('Rajshahi', 'Rajshahi'),
        ('Comilla', 'Comilla'),
        ('Chittagong', 'Chittagong'),
        ('Barisal', 'Barisal'),
        ('Dinajpur', 'Dinajpur'),
        ('Jessore', 'Jessore'),
        ('Mymensingh', 'Mymensingh'),
        ('Khulna', 'Khulna'),
        ('Sylhet', 'Sylhet'),
        ('Madrasah', 'Madrasah'),
        ('Technical', 'Technical'),
        ('Others', 'Others'),
    ])
    ssc_year = models.CharField(max_length=4, choices=[
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
        ('2028', '2028'),
        ('2029', '2029'),
    ])
    sscInstitution = models.CharField(max_length=100, null=True, blank=True)
    sscRoll = models.IntegerField(null=True, blank=True)
    sscReg = models.IntegerField(null=True, blank=True)
    ssc_session = models.ForeignKey(SscSession, on_delete=models.SET_NULL, null=True, blank=True, related_name='academic_infos_arts')
    sscGpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    compulsorySubjects = models.ManyToManyField(HscArtsCompulsorySubjects, related_name='academic_infos_compulsory_arts')
    optionalSubjects = models.ManyToManyField(HscArtsOptionalSubjects, related_name='academic_infos_optional_arts')
    mainSubjects = models.ForeignKey(HscArtsMainSubjects, on_delete=models.SET_NULL, null=True, blank=True, related_name='academic_infos_main_arts')
    FourSubjects = models.ForeignKey(HscArtsFourthSubjects, on_delete=models.SET_NULL, null=True, blank=True, related_name='academic_infos_four_arts')

    def __str__(self):
        return f"Academic Info of {self.student.name}"
    
class PaymentArts(models.Model):
    student = models.OneToOneField(HscAdmissionArts, on_delete=models.CASCADE, related_name='payment_arts')
    method = models.CharField(max_length=20, choices=[('Cash', 'Cash'), ('Bkash', 'Bkash'), ('Nagad', 'Nagad'), ('Rocket', 'Rocket')], null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Failed', 'Failed')], default='Pending')
    receipt_number = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return f"Payment for {self.student.name} - {self.amount} BDT"


    
# Commerce section

class HscCommerceCompulsorySubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class HscCommerceOptionalSubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class HscCommerceMainSubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class HscCommerceFourthSubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"
    

class HscAdmissionCommerce(models.Model):
    program = models.CharField(max_length=20, default='HSC', editable=False)
    type = models.CharField(max_length=10, default='Business', editable=False)
    ssc_roll = models.IntegerField(unique=True)
    hsc_session = models.ForeignKey(HscSession, on_delete=models.CASCADE)
    class_roll = models.IntegerField(unique=True)
    merit_position = models.IntegerField()
    name = models.CharField(max_length=100)
    name_bangla = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=11, validators=[numeric_validator])
    blood_group = models.CharField(max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
    ])
    birth_certificate_no = models.CharField(max_length=50)
    birthdate = models.DateField()
    marital_status = models.CharField(max_length=10, choices=[
        ('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'),
    ])
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'),
    ])
    nationality = models.CharField(max_length=50)
    religion = models.CharField(max_length=20, choices=[
        ('Islam', 'Islam'), ('Hindu', 'Hindu'), ('Christian', 'Christian'),
        ('Buddhist', 'Buddhist'), ('Other', 'Other'),
    ])
    photo = models.ImageField(upload_to='hsc-commerce/')

    def __str__(self):
        return f"Name: {self.name} | Group: Commerce | Class Roll: {self.class_roll} | Session: {self.hsc_session.session}"
    

class ParentInfoCommerce(models.Model):
    student = models.OneToOneField(HscAdmissionCommerce, on_delete=models.CASCADE, related_name='parent_info_commerce')
    fathers_name_english = models.CharField(max_length=100)
    fathers_nid = models.CharField(max_length=17, unique=True)
    fathers_date_of_birth = models.DateField()
    fathers_mobile = models.CharField(max_length=11, validators=[numeric_validator])
    father_occupation = models.CharField(max_length=50)
    fathers_monthly_income = models.IntegerField()
    mother_name_english = models.CharField(max_length=100)
    mothers_nid = models.CharField(max_length=17, unique=True)
    mothers_date_of_birth = models.DateField()
    mothers_mobile = models.CharField(max_length=11, validators=[numeric_validator])
    mother_occupation = models.CharField(max_length=50, blank=True)
    mothers_monthly_income = models.IntegerField()
    guardian = models.CharField(max_length=10, choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Other', 'Other')])
    guardian_name_english = models.CharField(max_length=100, null=True, blank=True)
    guardian_date_of_birth = models.DateField(null=True, blank=True)
    guardian_mobile = models.CharField(max_length=11, validators=[numeric_validator], null=True, blank=True)
    guardian_nid = models.CharField(max_length=17, unique=True, null=True, blank=True)

    def __str__(self):
        return f"Parents of {self.student.name}"


class AddressCommerce(models.Model):
    student = models.OneToOneField(HscAdmissionCommerce, on_delete=models.CASCADE, related_name='address_commerce')
    wardNo = models.IntegerField(null=True, blank=True)
    postOffice = models.CharField(max_length=50, null=True, blank=True)
    policeStation = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.IntegerField()
    permanent_address_same = models.BooleanField(default=False)
    permanent_wardNo = models.IntegerField(null=True, blank=True)
    permanent_postOffice = models.CharField(max_length=50, null=True, blank=True)
    permanent_policeStation = models.CharField(max_length=50, null=True, blank=True)
    permanent_district = models.CharField(max_length=50, null=True, blank=True)
    permanent_postal_code = models.IntegerField(null=True, blank=True)
    qouta_freedom = models.BooleanField(default=False)
    qouta_community = models.BooleanField(default=False)

    def __str__(self):
        return f"Address of {self.student.name}"


class AcademicInformationCommerce(models.Model):
    student = models.OneToOneField(HscAdmissionCommerce, on_delete=models.CASCADE, related_name='academic_info_commerce')
    ssc_board = models.CharField(max_length=20, choices=[
        ('Dhaka', 'Dhaka'),
        ('Rajshahi', 'Rajshahi'),
        ('Comilla', 'Comilla'),
        ('Chittagong', 'Chittagong'),
        ('Barisal', 'Barisal'),
        ('Dinajpur', 'Dinajpur'),
        ('Jessore', 'Jessore'),
        ('Mymensingh', 'Mymensingh'),
        ('Khulna', 'Khulna'),
        ('Sylhet', 'Sylhet'),
        ('Madrasah', 'Madrasah'),
        ('Technical', 'Technical'),
        ('Others', 'Others'),
    ])
    ssc_year = models.CharField(max_length=4, choices=[
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
        ('2028', '2028'),
        ('2029', '2029'),
    ])
    sscInstitution = models.CharField(max_length=100, null=True, blank=True)
    sscRoll = models.IntegerField(null=True, blank=True)
    sscReg = models.IntegerField(null=True, blank=True)
    ssc_session = models.ForeignKey(SscSession, on_delete=models.SET_NULL, null=True, blank=True, related_name='academic_infos_commerce')
    sscGpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    compulsorySubjects = models.ManyToManyField(HscCommerceCompulsorySubjects, related_name='academic_infos_compulsory_commerce')
    optionalSubjects = models.ManyToManyField(HscCommerceOptionalSubjects, related_name='academic_infos_optional_commerce')
    mainSubjects = models.ForeignKey(HscCommerceMainSubjects, on_delete=models.SET_NULL, null=True, blank=True, related_name='academic_infos_main_commerce')
    FourSubjects = models.ForeignKey(HscCommerceFourthSubjects, on_delete=models.SET_NULL, null=True, blank=True, related_name='academic_infos_four_commerce')

    def __str__(self):
        return f"Academic Info of {self.student.name}"
    
class PaymentCommerce(models.Model):
    student = models.OneToOneField(HscAdmissionCommerce, on_delete=models.CASCADE, related_name='payment_commerce')
    method = models.CharField(max_length=20, choices=[('Cash', 'Cash'), ('Bkash', 'Bkash'), ('Nagad', 'Nagad'), ('Rocket', 'Rocket')], null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Failed', 'Failed')], default='Pending')
    receipt_number = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return f"Payment for {self.student.name} - {self.amount} BDT"