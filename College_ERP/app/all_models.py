from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, EmailValidator
from common.models import BaseModel
from datetime import date

# Core Models
class Department(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    established_year = models.IntegerField(default=2020)
    head_of_department = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

class Program(BaseModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    duration_years = models.IntegerField(default=4)
    total_seats = models.IntegerField(default=60)
    description = models.TextField(blank=True)
    eligibility_criteria = models.TextField(blank=True)

    class Meta:
        ordering = ['department', 'name']

    def __str__(self):
        return f"{self.name} - {self.department.code}"

class Teacher(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=50)
    qualification = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200, blank=True)
    experience_years = models.IntegerField(default=0)
    joining_date = models.DateField(default=date.today)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.employee_id})"

class Staff(BaseModel):
    ROLE_CHOICES = [
        ('admissions_officer', 'Admissions Officer'),
        ('finance_officer', 'Finance Officer'),
        ('accounts_clerk', 'Accounts Clerk'),
        ('hostel_warden', 'Hostel Warden'),
        ('exam_controller', 'Exam Controller'),
        ('librarian', 'Librarian'),
        ('registrar', 'Registrar'),
        ('dean', 'Dean'),
        ('principal', 'Principal'),
        ('admin_staff', 'Administrative Staff'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    joining_date = models.DateField(default=date.today)
    is_active = models.BooleanField(default=True)
    
    # Role-based permissions
    can_access_admissions = models.BooleanField(default=False)
    can_access_hostel = models.BooleanField(default=False)
    can_access_finance = models.BooleanField(default=False)
    can_access_exams = models.BooleanField(default=False)
    can_access_library = models.BooleanField(default=False)
    can_access_students = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.staff_id}) - {self.get_role_display()}"

class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    admission_date = models.DateField(default=date.today)
    current_semester = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    guardian_email = models.EmailField(blank=True)

    class Meta:
        ordering = ['registration_number']

    def __str__(self):
        return f"{self.name} ({self.registration_number})"

class Document(BaseModel):
    DOCUMENT_TYPES = [
        ('academic_certificate', 'Academic Certificate'),
        ('identity_proof', 'Identity Proof'),
        ('address_proof', 'Address Proof'),
        ('photo', 'Photograph'),
        ('signature', 'Signature'),
        ('migration_certificate', 'Migration Certificate'),
        ('character_certificate', 'Character Certificate'),
        ('caste_certificate', 'Caste Certificate'),
        ('income_certificate', 'Income Certificate'),
        ('other', 'Other'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    document_name = models.CharField(max_length=200)
    file_path = models.FileField(upload_to='documents/')
    uploaded_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    verified_date = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-uploaded_date']

    def __str__(self):
        return f"{self.student.name} - {self.get_document_type_display()}"

# Admissions Models
class Application(BaseModel):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('waitlisted', 'Waitlisted'),
        ('admitted', 'Admitted'),
    ]

    application_number = models.CharField(max_length=20, unique=True)
    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    application_date = models.DateTimeField(auto_now_add=True)
    documents_submitted = models.BooleanField(default=False)
    entrance_score = models.FloatField(null=True, blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    admission_fee_paid = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-application_date']

    def __str__(self):
        return f"{self.application_number} - {self.student_name}"

# Finance Models
class FeeStructure(BaseModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    semester = models.IntegerField()
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hostel_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    library_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lab_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    exam_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    development_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def total_fee(self):
        return (self.tuition_fee + self.hostel_fee + self.library_fee + 
                self.lab_fee + self.exam_fee + self.development_fee + self.other_fee)

    class Meta:
        unique_together = ['program', 'semester']
        ordering = ['program', 'semester']

    def __str__(self):
        return f"{self.program} - Semester {self.semester}"

class Payment(BaseModel):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, default='online')
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    receipt_number = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.student.name} - {self.receipt_number}"

# Hostel Models
class HostelBlock(BaseModel):
    name = models.CharField(max_length=50)
    block_type = models.CharField(max_length=20, choices=[('boys', 'Boys'), ('girls', 'Girls')])
    total_rooms = models.IntegerField()
    warden_name = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.name} ({self.block_type.title()})"

class Room(BaseModel):
    block = models.ForeignKey(HostelBlock, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField(default=2)
    current_occupancy = models.IntegerField(default=0)
    room_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    amenities = models.TextField(blank=True)

    class Meta:
        unique_together = ['block', 'room_number']

    def __str__(self):
        return f"{self.block.name} - Room {self.room_number}"

class HostelAllocation(BaseModel):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    allocation_date = models.DateField(auto_now_add=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.name} - {self.room}"

# Exam Models
class Subject(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    semester = models.IntegerField()
    credits = models.IntegerField(default=3)
    theory_hours = models.IntegerField(default=3)
    practical_hours = models.IntegerField(default=0)

    class Meta:
        unique_together = ['code', 'program']
        ordering = ['program', 'semester', 'name']

    def __str__(self):
        return f"{self.code} - {self.name}"

class Exam(BaseModel):
    EXAM_TYPES = [
        ('mid_term', 'Mid Term'),
        ('end_term', 'End Term'),
        ('supplementary', 'Supplementary'),
        ('improvement', 'Improvement'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    exam_date = models.DateField()
    start_time = models.TimeField()
    duration_minutes = models.IntegerField(default=180)
    max_marks = models.IntegerField(default=100)
    room_number = models.CharField(max_length=20, blank=True)

    class Meta:
        unique_together = ['subject', 'exam_type', 'exam_date']
        ordering = ['exam_date', 'start_time']

    def __str__(self):
        return f"{self.subject.code} - {self.get_exam_type_display()}"

class Grade(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    grade_letter = models.CharField(max_length=2, blank=True)
    grade_point = models.FloatField(null=True, blank=True)
    is_pass = models.BooleanField(default=True)
    remarks = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ['student', 'exam']
        ordering = ['exam__exam_date']

    def __str__(self):
        return f"{self.student.name} - {self.exam.subject.code}: {self.marks_obtained}"

# Dashboard Stats Model
class DashboardStats(models.Model):
    total_students = models.IntegerField(default=0)
    total_teachers = models.IntegerField(default=0)
    total_staff = models.IntegerField(default=0)
    total_departments = models.IntegerField(default=0)
    total_programs = models.IntegerField(default=0)
    active_students = models.IntegerField(default=0)
    active_teachers = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Dashboard Statistics"
        verbose_name_plural = "Dashboard Statistics"
    
    @classmethod
    def update_stats(cls):
        stats, created = cls.objects.get_or_create(id=1)
        stats.total_students = Student.objects.count()
        stats.total_teachers = Teacher.objects.count()
        stats.total_staff = Staff.objects.count()
        stats.total_departments = Department.objects.count()
        stats.total_programs = Program.objects.count()
        stats.active_students = Student.objects.filter(is_active=True).count()
        stats.active_teachers = Teacher.objects.filter(is_active=True).count()
        stats.save()
        return stats