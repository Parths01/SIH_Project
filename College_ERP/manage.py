#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.core.management.base import BaseCommand


def create_superuser():
    """Create default superuser if it doesn't exist"""
    from django.contrib.auth.models import User
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@college.edu',
            password='admin123'
        )
        print("Created default superuser: admin/admin123")


def setup_initial_data():
    """Set up initial data for the system"""
    from app.models import Department, Program
    from finance.models import FeeHead
    from common.models import Settings
    
    # Create default department
    dept, created = Department.objects.get_or_create(
        code='CSE',
        defaults={
            'name': 'Computer Science & Engineering',
            'description': 'Department of Computer Science & Engineering'
        }
    )
    if created:
        print(f"Created department: {dept}")
    
    # Create default program
    program, created = Program.objects.get_or_create(
        code='BTECH_CSE',
        defaults={
            'name': 'B.Tech Computer Science & Engineering',
            'department': dept,
            'degree_type': 'UG',
            'duration_years': 4,
            'total_semesters': 8,
            'min_credits': 160
        }
    )
    if created:
        print(f"Created program: {program}")
    
    # Create default fee heads
    fee_heads = [
        ('TUITION', 'Tuition Fee'),
        ('EXAM', 'Examination Fee'),
        ('LIBRARY', 'Library Fee'),
        ('LAB', 'Laboratory Fee'),
        ('HOSTEL', 'Hostel Fee'),
        ('MESS', 'Mess Fee'),
        ('DEVELOPMENT', 'Development Fee'),
        ('ADMISSION', 'Admission Fee'),
    ]
    
    for code, name in fee_heads:
        head, created = FeeHead.objects.get_or_create(
            code=code,
            defaults={'name': name}
        )
        if created:
            print(f"Created fee head: {head}")
    
    # Create system settings
    settings_data = [
        ('ACADEMIC_YEAR', '2024-25', 'Current Academic Year'),
        ('CURRENT_SEMESTER', '1', 'Current Semester'),
        ('LATE_FEE_GRACE_DAYS', '7', 'Grace days for late fee'),
        ('LATE_FEE_AMOUNT', '500', 'Late fee amount per day'),
        ('EMAIL_ENABLED', 'True', 'Enable email notifications'),
        ('SMS_ENABLED', 'False', 'Enable SMS notifications'),
    ]
    
    for key, value, desc in settings_data:
        setting, created = Settings.objects.get_or_create(
            key=key,
            defaults={'value': value, 'description': desc}
        )
        if created:
            print(f"Created setting: {setting}")


class Command(BaseCommand):
    help = 'Initialize the system with default data'
    
    def handle(self, *args, **options):
        create_superuser()
        setup_initial_data()
        print("System initialization completed!")


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'College_ERP.settings')
    
    # Check if this is the initialization command
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        django.setup()
        cmd = Command()
        cmd.handle()
    else:
        execute_from_command_line(sys.argv)
