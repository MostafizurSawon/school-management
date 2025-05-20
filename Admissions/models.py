from django.db import models
from django.core.validators import RegexValidator

numeric_validator = RegexValidator(r'^\d{11}$', 'Enter a valid 11-digit number.')

class HscSession(models.Model):
    session = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return self.session
    
class HscScienceSubjects(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"
    
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
    photo = models.ImageField(upload_to='hsc_science/')

    def __str__(self):
        return f"Name: {self.name} | Group: Science | Class Roll: {self.class_roll} | Session: {self.hsc_session.session}"

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
    photo = models.ImageField(upload_to='hsc_commerce/')

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
    photo = models.ImageField(upload_to='hsc_arts/')

    def __str__(self):
        return f"Name: {self.name} | Group: Arts | Class Roll: {self.class_roll} | Session: {self.hsc_session.session}"

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
    wardNo = models.IntegerField()
    postOffice = models.CharField(max_length=50)
    policeStation = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

    permanent_address = models.TextField()
    present_address = models.TextField()
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default='Bangladesh')

    def __str__(self):
        return f"Address of {self.student.name}"

class AcademicInformation(models.Model):
    student = models.OneToOneField(HscAdmissionScience, on_delete=models.CASCADE, related_name='academic_info')
    ssc_board = models.CharField(max_length=50)
    ssc_year = models.IntegerField()
    ssc_gpa = models.FloatField()
    ssc_certificate = models.FileField(upload_to='hsc_science/certificates/', blank=True)

    def __str__(self):
        return f"Academic Info of {self.student.name}"

class Payment(models.Model):
    student = models.OneToOneField(HscAdmissionScience, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ], default='Pending')
    receipt_number = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return f"Payment for {self.student.name} - {self.amount} BDT"