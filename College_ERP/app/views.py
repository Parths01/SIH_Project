from django.shortcuts import render
from django.http import HttpResponse

# Custom admin dashboard view - completely independent of Django admin
def admin_dashboard(request):
    """Custom ERP dashboard - standalone"""
    
    # Get statistics for the dashboard
    try:
        from .models import Student, Teacher, Staff, Department, Program, Document
        
        stats = {
            'total_students': Student.objects.count(),
            'active_students': Student.objects.filter(is_active=True).count(),
            'total_teachers': Teacher.objects.count(),
            'active_teachers': Teacher.objects.filter(is_active=True).count(),
            'total_staff': Staff.objects.count(),
            'active_staff': Staff.objects.filter(is_active=True).count(),
            'total_departments': Department.objects.count(),
            'total_programs': Program.objects.count(),
            'total_applications': 0,  # Will be updated when Application model is active
        }
    except Exception:
        # Fallback stats if models aren't migrated yet
        stats = {
            'total_students': 0,
            'active_students': 0,
            'total_teachers': 0,
            'active_teachers': 0,
            'total_staff': 0,
            'active_staff': 0,
            'total_departments': 0,
            'total_programs': 0,
            'total_applications': 0,
        }
    
    context = {
        'title': 'College ERP Dashboard',
        'stats': stats,
        'user': request.user,
    }
    
    return render(request, 'admin/dashboard.html', context)

# Simple placeholder views for ERP modules

def dashboard(request):
    """ERP Dashboard view"""
    return render(request, 'erp/dashboard.html', {'title': 'ERP Dashboard'})

def student_list(request):
    """Student list view"""
    return render(request, 'erp/students.html', {'title': 'Students'})

def faculty_list(request):
    """Faculty list view"""
    return render(request, 'erp/faculty.html', {'title': 'Faculty'})

def staff_list(request):
    """Staff list view"""
    return render(request, 'erp/staff.html', {'title': 'Staff'})

def department_list(request):
    """Department list view"""
    return render(request, 'erp/departments.html', {'title': 'Departments'})

def program_list(request):
    """Program list view"""
    return render(request, 'erp/programs.html', {'title': 'Programs'})
