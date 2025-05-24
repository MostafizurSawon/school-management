from django.db import models
from django.core.validators import RegexValidator

numeric_validator = RegexValidator(r'^\d{11}$', 'Enter a valid 11-digit number.')

class HscSession(models.Model):
    session = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return self.session
    
class SscSession(models.Model):
    session = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return self.session

    
class HscScienceSubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_main = models.BooleanField(default=False)
    fourth = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_name} ({self.is_active})"

class HscAdmissionScience(models.Model):
    ssc_roll = models.IntegerField(unique=True)
    hsc_session = models.ForeignKey(HscSession, on_delete=models.CASCADE)
    class_roll = models.IntegerField(unique=True)
    merit_position = models.IntegerField()
    name = models.CharField(max_length=100)
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
    ssc_board = models.CharField(max_length=20,choices=[
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
    ssc_session = models.ForeignKey(
        SscSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='academic_infos'
    )

    sscGpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    compulsory_bangla = models.ForeignKey(HscScienceSubjects, on_delete=models.SET_NULL, null=True, related_name='compulsory_bangla')
    compulsory_english = models.ForeignKey(HscScienceSubjects, on_delete=models.SET_NULL, null=True, related_name='compulsory_english')
    compulsory_ict = models.ForeignKey(HscScienceSubjects, on_delete=models.SET_NULL, null=True, related_name='compulsory_ict')

    elective_physics = models.ForeignKey(HscScienceSubjects, on_delete=models.SET_NULL, null=True, related_name='elective_physics')
    elective_chemistry = models.ForeignKey(HscScienceSubjects, on_delete=models.SET_NULL, null=True, related_name='elective_chemistry')

    main_subject = models.ForeignKey(HscScienceSubjects, on_delete=models.SET_NULL, null=True, related_name='main_subject')  # biology or higher math
    fourth_subject = models.ForeignKey(HscScienceSubjects, on_delete=models.SET_NULL, null=True, related_name='fourth_subject')

    def __str__(self):
        return f"Academic Info of {self.student.name}"

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




class HscArtsSubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"
    
class HscCommerceSubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"
    

class HscAdmissionCommerce(models.Model):
    ssc_roll = models.IntegerField(unique=True)
    hsc_session = models.ForeignKey(HscSession, on_delete=models.CASCADE)
    class_roll = models.IntegerField(unique=True)
    merit_position = models.IntegerField()
    name = models.CharField(max_length=100)
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
    photo = models.ImageField(upload_to='hsc-commerce/')

    def __str__(self):
        return f"Name: {self.name} | Group: Commerce | Class Roll: {self.class_roll} | Session: {self.hsc_session.session}"

class HscAdmissionArts(models.Model):
    ssc_roll = models.IntegerField(unique=True)
    hsc_session = models.ForeignKey(HscSession, on_delete=models.CASCADE)
    class_roll = models.IntegerField(unique=True)
    merit_position = models.IntegerField()
    name = models.CharField(max_length=100)
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
    photo = models.ImageField(upload_to='hsc-arts/')

    def __str__(self):
        return f"Name: {self.name} | Group: Arts | Class Roll: {self.class_roll} | Session: {self.hsc_session.session}"
