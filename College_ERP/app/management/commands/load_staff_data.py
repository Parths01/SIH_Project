from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from app.models import Department, Staff
from datetime import date

class Command(BaseCommand):
    help = 'Load staff data with role-based permissions'

    def handle(self, *args, **options):
        self.stdout.write('🏢 Loading staff data with restricted access...')
        
        # Create permission groups first
        self.create_permission_groups()
        
        # Staff data with specific roles and permissions
        staff_data = [
            # Admissions Staff - Only admissions access
            ('ADM001', 'Mrs. Sunita Sharma', 'admissions_officer', None, ['admissions', 'students'], date(2018, 6, 15)),
            ('ADM002', 'Mr. Rajesh Verma', 'admissions_officer', None, ['admissions'], date(2020, 7, 10)),
            
            # Hostel Staff - Only hostel access
            ('HOS001', 'Dr. Meera Kulkarni', 'hostel_warden', None, ['hostel', 'students'], date(2016, 8, 1)),
            ('HOS002', 'Mrs. Priya Joshi', 'hostel_warden', None, ['hostel'], date(2019, 9, 15)),
            
            # Finance Staff - Only finance access
            ('FIN001', 'CA Amit Patel', 'finance_officer', None, ['finance', 'students'], date(2015, 5, 20)),
            ('FIN002', 'Mrs. Kavita Desai', 'accounts_clerk', None, ['finance'], date(2021, 4, 10)),
            
            # Exam Staff - Only exam access
            ('EXM001', 'Prof. Suresh Kumar', 'exam_controller', 'SET', ['exams', 'students'], date(2012, 3, 25)),
            ('EXM002', 'Dr. Anjali Gupta', 'exam_controller', 'SCSE', ['exams', 'students'], date(2017, 2, 18)),
            
            # Library Staff - Only library access
            ('LIB001', 'Mrs. Shilpa Agrawal', 'librarian', None, ['library', 'students'], date(2014, 7, 5)),
            
            # Senior Management - Multiple access
            ('REG001', 'Dr. Vikram Singh', 'registrar', None, ['admissions', 'students', 'exams'], date(2010, 1, 15)),
            ('DEAN001', 'Dr. Ashok Pandey', 'dean', 'SET', ['students', 'exams', 'admissions'], date(2008, 6, 1)),
            ('PRIN001', 'Dr. Radhika Nair', 'principal', None, ['admissions', 'hostel', 'finance', 'exams', 'library', 'students'], date(2005, 4, 1)),
        ]
        
        created_count = 0
        existing_count = 0
        
        for staff_id, name, role, dept_code, access_modules, joining_date in staff_data:
            try:
                # Find department if specified
                department = None
                if dept_code:
                    department = Department.objects.filter(code=dept_code).first()
                
                # Check if staff already exists
                if Staff.objects.filter(staff_id=staff_id).exists():
                    existing_count += 1
                    self.stdout.write(f'Staff already exists: {name} ({staff_id})')
                    continue
                
                # Create username from staff name
                username = name.lower().replace('mrs. ', '').replace('mr. ', '').replace('dr. ', '').replace('prof. ', '').replace('ca ', '').replace(' ', '_')
                
                # Create user
                user, user_created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': name.split()[-2] if len(name.split()) > 2 else name.split()[0],
                        'last_name': name.split()[-1],
                        'email': f'{username}@college.edu',
                        'is_staff': True,  # Staff access to admin
                    }
                )
                
                if user_created:
                    user.set_password('staff123')
                    user.save()
                
                # Set access permissions based on role
                access_permissions = {
                    'can_access_admissions': 'admissions' in access_modules,
                    'can_access_hostel': 'hostel' in access_modules,
                    'can_access_finance': 'finance' in access_modules,
                    'can_access_exams': 'exams' in access_modules,
                    'can_access_library': 'library' in access_modules,
                    'can_access_students': 'students' in access_modules,
                }
                
                # Create staff
                staff = Staff.objects.create(
                    user=user,
                    staff_id=staff_id,
                    name=name,
                    email=f'{username}@college.edu',
                    phone=f'9876{staff_id[-3:]}222',
                    role=role,
                    department=department,
                    is_active=True,
                    joining_date=joining_date,
                    **access_permissions
                )
                
                # Assign to appropriate permission group
                group_name = f"{role.replace('_', ' ').title()} Group"
                try:
                    group = Group.objects.get(name=group_name)
                    user.groups.add(group)
                except Group.DoesNotExist:
                    pass
                
                created_count += 1
                modules_str = ', '.join(access_modules)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Created: {name} ({staff_id}) - {role} | Access: {modules_str}'
                    )
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error creating staff {name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Staff loading completed!\n'
                f'✅ Created: {created_count} staff members\n'
                f'⚠️  Already existed: {existing_count} staff members\n'
                f'🔑 Default password for all staff: staff123\n'
                f'🔒 Each staff member has restricted access to their modules only'
            )
        )

    def create_permission_groups(self):
        """Create permission groups for different staff roles"""
        self.stdout.write('🔐 Creating permission groups...')
        
        groups_and_permissions = {
            'Admissions Officer Group': ['admissions'],
            'Hostel Warden Group': ['hostel'],
            'Finance Officer Group': ['finance'],
            'Exam Controller Group': ['exams'],
            'Librarian Group': ['library'],
            'Registrar Group': ['admissions', 'students', 'exams'],
            'Dean Group': ['students', 'exams', 'admissions'],
            'Principal Group': ['admissions', 'hostel', 'finance', 'exams', 'library', 'students'],
        }
        
        for group_name, modules in groups_and_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'  ✅ Created group: {group_name}')
        
        self.stdout.write('✅ Permission groups created!')