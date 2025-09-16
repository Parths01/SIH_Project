from django.db import models
from django.contrib.auth.models import User
from common.models import BaseModel

class Department(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name

class Program(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    duration_years = models.PositiveIntegerField(default=4)
    
    def __str__(self):
        return f"{self.name} ({self.department.code})"

class Teacher(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, choices=[
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('hod', 'Head of Department'),
    ])
    qualification = models.CharField(max_length=200)
    experience_years = models.IntegerField(default=0)
    specialization = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    joining_date = models.DateField()
    
    def __str__(self):
        return f"{self.employee_id} - {self.name}"
    
    class Meta:
        ordering = ['employee_id']

class Staff(BaseModel):
    STAFF_ROLES = [
        ('admissions_officer', 'Admissions Officer'),
        ('hostel_warden', 'Hostel Warden'),
        ('finance_officer', 'Finance Officer'),
        ('exam_controller', 'Exam Controller'),
        ('librarian', 'Librarian'),
        ('accounts_clerk', 'Accounts Clerk'),
        ('registrar', 'Registrar'),
        ('dean', 'Dean'),
        ('principal', 'Principal'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=50, choices=STAFF_ROLES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    joining_date = models.DateField()
    
    # Access permissions for different modules
    can_access_admissions = models.BooleanField(default=False)
    can_access_hostel = models.BooleanField(default=False)
    can_access_finance = models.BooleanField(default=False)
    can_access_exams = models.BooleanField(default=False)
    can_access_library = models.BooleanField(default=False)
    can_access_students = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.staff_id} - {self.name} ({self.get_role_display()})"
    
    class Meta:
        ordering = ['staff_id']

class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    admission_date = models.DateField()
    current_semester = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.registration_number})"

class Document(BaseModel):
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=50, choices=[
        ('transcript', 'Transcript'),
        ('certificate', 'Certificate'),
        ('id_proof', 'ID Proof'),
        ('photo', 'Photo'),
        ('other', 'Other'),
    ])
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='documents/')
    file_size = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.student.name}"
