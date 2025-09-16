from django.urls import path
from . import views

# Simple ERP URLs - only basic ones for now
urlpatterns = [
    # Dashboard URL
    path('dashboard/', views.dashboard, name='erp_dashboard'),
    
    # Basic module URLs
    path('students/', views.student_list, name='student_list'),
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('staff/', views.staff_list, name='staff_list'),
    path('departments/', views.department_list, name='department_list'),
    path('programs/', views.program_list, name='program_list'),
]