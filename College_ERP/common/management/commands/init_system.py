from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.db import transaction
import os


class Command(BaseCommand):
    help = 'Initialize the College ERP system with default data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force initialization even if data exists',
        )

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                self.stdout.write(
                    self.style.SUCCESS('Starting College ERP System initialization...')
                )
                
                # Create superuser
                self._create_superuser(options['force'])
                
                # Create user groups/roles
                self._create_user_groups()
                
                # Create default academic structure
                self._create_academic_structure()
                
                # Create fee structure
                self._create_fee_structure()
                
                # Create system settings
                self._create_system_settings()
                
                # Create default hostel structure
                self._create_hostel_structure()
                
                # Create grade scale
                self._create_grade_scale()
                
                self.stdout.write(
                    self.style.SUCCESS('✅ College ERP System initialized successfully!')
                )
                self.stdout.write(
                    self.style.WARNING('Default admin credentials: admin / admin123')
                )
                self.stdout.write(
                    self.style.WARNING('Please change the default password after first login!')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Initialization failed: {str(e)}')
            )
            raise CommandError(f'Initialization failed: {str(e)}')

    def _create_superuser(self, force=False):
        """Create default superuser"""
        if User.objects.filter(username='admin').exists() and not force:
            self.stdout.write('👤 Admin user already exists, skipping...')
            return
        
        if force:
            User.objects.filter(username='admin').delete()
        
        User.objects.create_superuser(
            username='admin',
            email=os.getenv('ADMIN_EMAIL', 'admin@college.edu'),
            password='admin123',
            first_name='System',
            last_name='Administrator'
        )
        self.stdout.write('👤 Created default superuser: admin')

    def _create_user_groups(self):
        """Create user groups for role-based access"""
        groups = [
            ('Admissions Staff', 'Manage admissions and applications'),
            ('Finance Staff', 'Manage fees and payments'),
            ('Hostel Warden', 'Manage hostel allocations'),
            ('Exam Staff', 'Manage examinations and results'),
            ('Faculty', 'Teaching staff'),
            ('Students', 'Student users'),
            ('Department Head', 'Department administration'),
            ('Principal', 'Institution head'),
        ]
        
        for group_name, description in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'👥 Created user group: {group_name}')

    def _create_academic_structure(self):
        """Create default academic structure"""
        from app.models import Department, Program
        
        # Create departments
        departments_data = [
            ('CSE', 'Computer Science & Engineering'),
            ('ECE', 'Electronics & Communication Engineering'),
            ('ME', 'Mechanical Engineering'),
            ('CE', 'Civil Engineering'),
            ('EEE', 'Electrical & Electronics Engineering'),
        ]
        
        for code, name in departments_data:
            dept, created = Department.objects.get_or_create(
                code=code,
                defaults={'name': name, 'description': f'Department of {name}'}
            )
            if created:
                self.stdout.write(f'🏫 Created department: {code} - {name}')
        
        # Create programs
        programs_data = [
            ('BTECH_CSE', 'B.Tech Computer Science & Engineering', 'CSE', 'UG', 4, 8),
            ('BTECH_ECE', 'B.Tech Electronics & Communication', 'ECE', 'UG', 4, 8),
            ('MTECH_CSE', 'M.Tech Computer Science & Engineering', 'CSE', 'PG', 2, 4),
            ('MBA', 'Master of Business Administration', 'CSE', 'PG', 2, 4),
        ]
        
        for code, name, dept_code, degree_type, duration, semesters in programs_data:
            try:
                department = Department.objects.get(code=dept_code)
                program, created = Program.objects.get_or_create(
                    code=code,
                    defaults={
                        'name': name,
                        'department': department,
                        'degree_type': degree_type,
                        'duration_years': duration,
                        'total_semesters': semesters,
                        'min_credits': 160 if degree_type == 'UG' else 80
                    }
                )
                if created:
                    self.stdout.write(f'📚 Created program: {code} - {name}')
            except Department.DoesNotExist:
                self.stdout.write(f'⚠️  Department {dept_code} not found for program {code}')

    def _create_fee_structure(self):
        """Create default fee heads"""
        from finance.models import FeeHead
        
        fee_heads_data = [
            ('TUITION', 'Tuition Fee', True, 'INCOME_TUITION'),
            ('EXAM', 'Examination Fee', True, 'INCOME_EXAM'),
            ('LIBRARY', 'Library Fee', True, 'INCOME_LIBRARY'),
            ('LAB', 'Laboratory Fee', True, 'INCOME_LAB'),
            ('DEVELOPMENT', 'Development Fee', False, 'INCOME_DEVELOPMENT'),
            ('ADMISSION', 'Admission Fee', False, 'INCOME_ADMISSION'),
            ('HOSTEL', 'Hostel Fee', True, 'INCOME_HOSTEL'),
            ('MESS', 'Mess Fee', True, 'INCOME_MESS'),
            ('TRANSPORT', 'Transport Fee', True, 'INCOME_TRANSPORT'),
            ('CAUTION', 'Caution Deposit', False, 'LIABILITY_CAUTION'),
        ]
        
        for code, name, recurring, gl_code in fee_heads_data:
            head, created = FeeHead.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'is_recurring': recurring,
                    'gl_account_code': gl_code
                }
            )
            if created:
                self.stdout.write(f'💰 Created fee head: {code} - {name}')

    def _create_system_settings(self):
        """Create system settings"""
        from common.models import Settings
        
        settings_data = [
            ('ACADEMIC_YEAR', '2024-25', 'Current Academic Year'),
            ('CURRENT_SEMESTER', '1', 'Current Semester'),
            ('LATE_FEE_GRACE_DAYS', '7', 'Grace days before late fee'),
            ('LATE_FEE_AMOUNT', '100', 'Late fee amount per day'),
            ('EMAIL_NOTIFICATIONS', 'True', 'Enable email notifications'),
            ('SMS_NOTIFICATIONS', 'False', 'Enable SMS notifications'),
            ('AUTO_RECEIPT_GENERATION', 'True', 'Auto-generate receipts'),
            ('BACKUP_ENABLED', 'True', 'Enable automatic backups'),
            ('MAX_FILE_SIZE_MB', '10', 'Maximum file upload size in MB'),
            ('PAYMENT_GATEWAY', 'razorpay', 'Default payment gateway'),
        ]
        
        for key, value, description in settings_data:
            setting, created = Settings.objects.get_or_create(
                key=key,
                defaults={'value': value, 'description': description}
            )
            if created:
                self.stdout.write(f'⚙️  Created setting: {key}')

    def _create_hostel_structure(self):
        """Create sample hostel structure"""
        from hostel.models import Hostel, Room
        
        # Create hostels
        hostels_data = [
            ('Boys Hostel A', 'BHA', 'M', 100, 'Campus Block A'),
            ('Girls Hostel A', 'GHA', 'F', 80, 'Campus Block B'),
        ]
        
        for name, code, gender, capacity, address in hostels_data:
            hostel, created = Hostel.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'gender': gender,
                    'total_capacity': capacity,
                    'address': address,
                    'mess_facility': True
                }
            )
            if created:
                self.stdout.write(f'🏠 Created hostel: {code} - {name}')
                
                # Create sample rooms
                for floor in range(1, 4):  # 3 floors
                    for room_num in range(1, 11):  # 10 rooms per floor
                        room_number = f'{floor}{room_num:02d}'
                        Room.objects.create(
                            hostel=hostel,
                            room_number=room_number,
                            floor=floor,
                            room_type='double',
                            capacity=2,
                            monthly_rent=3000.00,
                            security_deposit=5000.00,
                            has_attached_bathroom=True,
                            furnished=True
                        )
                self.stdout.write(f'🛏️  Created 30 sample rooms for {name}')

    def _create_grade_scale(self):
        """Create standard grading scale"""
        from exams.models import GradeScale
        
        grades_data = [
            (90, 100, 'A+', 10.0, 'Outstanding', True),
            (85, 89, 'A', 9.0, 'Excellent', True),
            (80, 84, 'B+', 8.0, 'Very Good', True),
            (75, 79, 'B', 7.0, 'Good', True),
            (70, 74, 'C+', 6.0, 'Above Average', True),
            (65, 69, 'C', 5.0, 'Average', True),
            (60, 64, 'D', 4.0, 'Below Average', True),
            (50, 59, 'E', 3.0, 'Poor', True),
            (0, 49, 'F', 0.0, 'Fail', False),
        ]
        
        for min_pct, max_pct, grade, points, desc, passing in grades_data:
            grade_obj, created = GradeScale.objects.get_or_create(
                grade=grade,
                defaults={
                    'name': f'{grade} Grade',
                    'min_percentage': min_pct,
                    'max_percentage': max_pct,
                    'grade_points': points,
                    'description': desc,
                    'is_passing': passing
                }
            )
            if created:
                self.stdout.write(f'🎓 Created grade: {grade} ({min_pct}-{max_pct}%)')