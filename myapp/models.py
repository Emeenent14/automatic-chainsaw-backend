from django.db import models
import os
import uuid

def get_file_path(instance, filename):
    """Custom function to generate unique file paths for uploaded images."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('passports', filename)

class StudentSubmission(models.Model):
    """Model to store student registration form data."""
    # Personal Information
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    othername = models.CharField(max_length=100, blank=True)
    sex = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    whatsapp_name = models.CharField(max_length=100, blank=True)
    nationality = models.CharField(max_length=100)
    passport = models.ImageField(upload_to=get_file_path)
    
    # Academic Details
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    level_of_study = models.CharField(max_length=20)
    matric_number = models.CharField(max_length=50)
    
    # Residential Info
    permanent_address = models.TextField()
    accommodation_type = models.CharField(max_length=20)
    residential_address = models.TextField()
    state_of_residence = models.CharField(max_length=100)
    lga_of_residence = models.CharField(max_length=100)
    
    # Guardian Information
    guardian_name = models.CharField(max_length=200)
    guardian_phone_number = models.CharField(max_length=20)
    
    # Others
    religion = models.CharField(max_length=20)
    state_of_origin = models.CharField(max_length=100)
    local_government = models.CharField(max_length=100)
    skills = models.TextField(blank=True)
    extracurricular_activities = models.TextField()

    # New fields:
    second_phone_number = models.CharField(max_length=20, blank=True)
    marital_status = models.CharField(max_length=10, choices=[('Single', 'Single'), ('Married', 'Married')], blank=True, null=True)
    mode_of_entry = models.CharField(max_length=20, choices=[('UTME', 'UTME'), ('Direct Entry', 'Direct Entry'), ('Transfer', 'Transfer')],  blank=True, null=True )
    jamb_reg_number = models.CharField(max_length=50, blank=True)
    next_of_kin_name = models.CharField(max_length=200, blank=True, null=True )
    next_of_kin_phone = models.CharField(max_length=20,  blank=True, null=True)
    next_of_kin_relationship = models.CharField(max_length=100, blank=True, null=True)
    
    # Submission information
    submission_code = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        default=lambda: f"EMT{uuid.uuid4().hex[:6].upper()}"
    )
    submission_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.firstname} {self.surname} ({self.submission_code})"
    
    class Meta:
        ordering = ['-submission_date']