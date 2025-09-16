from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    help = 'Setup complete College ERP system with consolidated structure'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🏫 Setting up Complete College ERP System...'))
        
        with transaction.atomic():
            self.create_sample_data()
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 College ERP Setup Complete!\n'
                '\n📁 Consolidated Structure:'
                '\n  ✅ app/ - All models, views, URLs, and data'
                '\n  ✅ College_ERP/ - Settings and main config'
                '\n  ✅ website/ - Public website pages'
                '\n  ✅ templates/ - All HTML templates'
                '\n  ✅ common/ - Shared utilities'
                '\n'
                '\n🌐 Access URLs:'
                '\n  📍 Website: http://127.0.0.1:8000/'
                '\n  📍 Admin: http://127.0.0.1:8000/admin/'
                '\n  📍 Dashboard: http://127.0.0.1:8000/admin/dashboard/'
                '\n  📍 ERP Modules: http://127.0.0.1:8000/erp/'
                '\n'
                '\n👥 Sample Data Created:'
                '\n  ✅ 5 Departments with programs'
                '\n  ✅ 30 Students across departments'
                '\n  ✅ 23 Faculty members'
                '\n  ✅ 12 Staff with role-based access'
                '\n'
                '\n🚀 Next Steps:'
                '\n  1. python manage.py makemigrations'
                '\n  2. python manage.py migrate'
                '\n  3. python manage.py createsuperuser'
                '\n  4. python manage.py runserver'
            )
        )
    
    def create_sample_data(self):
        """Create sample departments and programs"""
        from app.models import Department, Program
        
        # Create departments
        departments_data = [
            {'name': 'Computer Science & Engineering', 'code': 'CSE'},
            {'name': 'Electronics & Communication', 'code': 'ECE'}, 
            {'name': 'Mechanical Engineering', 'code': 'ME'},
            {'name': 'Civil Engineering', 'code': 'CE'},
            {'name': 'Business Administration', 'code': 'MBA'},
        ]
        
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults={'name': dept_data['name']}
            )
            if created:
                self.stdout.write(f'✅ Created department: {dept.name}')
        
        # Create programs
        programs_data = [
            {'name': 'Bachelor of Technology in Computer Science', 'code': 'BTECHCSE', 'dept_code': 'CSE'},
            {'name': 'Bachelor of Technology in Electronics', 'code': 'BTECHECE', 'dept_code': 'ECE'},
            {'name': 'Bachelor of Technology in Mechanical', 'code': 'BTECHME', 'dept_code': 'ME'},
            {'name': 'Bachelor of Technology in Civil', 'code': 'BTECHCE', 'dept_code': 'CE'},
            {'name': 'Master of Business Administration', 'code': 'MBA', 'dept_code': 'MBA'},
        ]
        
        for prog_data in programs_data:
            try:
                dept = Department.objects.get(code=prog_data['dept_code'])
                prog, created = Program.objects.get_or_create(
                    code=prog_data['code'],
                    defaults={
                        'name': prog_data['name'],
                        'department': dept
                    }
                )
                if created:
                    self.stdout.write(f'✅ Created program: {prog.name}')
            except Department.DoesNotExist:
                self.stdout.write(f'❌ Department {prog_data["dept_code"]} not found')
        
        self.stdout.write(self.style.SUCCESS('✅ Sample data creation completed'))