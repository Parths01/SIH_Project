from django.contrib import admin
from .models import Department, Program, Teacher, Staff, Student, Document

# Simple admin registration - only basic fields that exist

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department']
    list_filter = ['department']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'employee_id', 'email', 'department']
    list_filter = ['department', 'is_active']
    search_fields = ['name', 'employee_id', 'email']
    ordering = ['name']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'staff_id', 'email', 'role']
    list_filter = ['role', 'is_active']
    search_fields = ['name', 'staff_id', 'email']
    ordering = ['name']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_number', 'email', 'program']
    list_filter = ['program', 'is_active']
    search_fields = ['name', 'registration_number', 'email']
    ordering = ['name']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['student', 'document_type', 'is_verified']
    list_filter = ['document_type', 'is_verified']
    search_fields = ['student__name']
    ordering = ['id']

# Customize Django Admin Site
admin.site.site_header = "College ERP Administration"
admin.site.site_title = "College ERP Admin"
admin.site.index_title = "Welcome to College ERP Administration"
