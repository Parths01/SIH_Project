from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Department, Program, Student
from datetime import date

class Command(BaseCommand):
    help = 'Load all initial data: departments, programs, and students'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Loading complete College ERP data...\n'))
        
        # First load departments and programs
        self.load_departments_and_programs()
        
        # Then load students
        self.load_students()
        
        self.stdout.write(self.style.SUCCESS('\n✅ All data loaded successfully!'))
        
    def load_departments_and_programs(self):
        self.stdout.write('📚 Loading departments and programs...')
        
        departments_data = [
            {
                'name': 'School of Engineering & Technology',
                'code': 'SET',
                'programs': [
                    ('B.Tech in Civil Engineering', 'BTCE', 4),
                    ('B.Tech in Mechanical Engineering', 'BTME', 4),
                    ('B.Tech in Electrical & Electronics Engineering', 'BTEEE', 4),
                    ('B.Tech in Electronics & Communication Engineering', 'BTECE', 4),
                    ('B.Tech in Chemical Engineering', 'BTCHE', 4),
                    ('B.Tech in Petroleum Engineering', 'BTPE', 4),
                    ('M.Tech (Various specializations)', 'MTECH', 2),
                ]
            },
            {
                'name': 'School of Computer Science & Engineering',
                'code': 'SCSE',
                'programs': [
                    ('B.Tech in Computer Science & Engineering', 'BTCSE', 4),
                    ('B.Tech in Artificial Intelligence & Data Science', 'BTAIDS', 4),
                    ('B.Tech in Cybersecurity', 'BTCS', 4),
                    ('B.Tech in Robotics & Automation', 'BTRA', 4),
                    ('M.Tech in Computer Science', 'MTCS', 2),
                    ('MCA (Master of Computer Applications)', 'MCA', 2),
                ]
            },
            {
                'name': 'School of Polytechnic',
                'code': 'SOP',
                'programs': [
                    ('Diploma in Mechanical Engineering', 'DME', 3),
                    ('Diploma in Civil Engineering', 'DCE', 3),
                    ('Diploma in Computer Engineering', 'DCOMP', 3),
                    ('Diploma in Electrical Engineering', 'DEE', 3),
                    ('Diploma in Electronics & Telecommunication', 'DET', 3),
                ]
            },
            {
                'name': 'School of Management',
                'code': 'SOM',
                'programs': [
                    ('BBA (General)', 'BBA', 3),
                    ('BBA (International Business)', 'BBAIB', 3),
                    ('BBA (Marketing / Finance / HR)', 'BBAMFH', 3),
                    ('MBA (Various specializations)', 'MBA', 2),
                ]
            },
            {
                'name': 'School of Economics & Commerce',
                'code': 'SEC',
                'programs': [
                    ('B.Com (General)', 'BCOM', 3),
                    ('B.Com (International Accounting & Finance)', 'BCOMIAF', 3),
                    ('B.A. (Hons) Economics', 'BAECO', 3),
                    ('M.Com', 'MCOM', 2),
                    ('M.A. Economics', 'MAECO', 2),
                ]
            },
        ]

        for dept_data in departments_data:
            department, created = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults={'name': dept_data['name']}
            )
            
            if created:
                self.stdout.write(f'  ✅ Created department: {department.name}')
            
            for program_name, program_code, duration in dept_data['programs']:
                program, created = Program.objects.get_or_create(
                    code=program_code,
                    defaults={
                        'name': program_name,
                        'department': department,
                        'duration_years': duration
                    }
                )
                
                if created:
                    self.stdout.write(f'    ✅ Created program: {program.name}')

    def load_students(self):
        self.stdout.write('\n👥 Loading student data...')
        
        students_data = [
            ('S001', 'Aarav Patil', 'B.Tech in Civil Engineering'),
            ('S002', 'Riya Kulkarni', 'B.Tech in Mechanical Engineering'),
            ('S003', 'Omkar Jadhav', 'B.Tech in Electrical & Electronics Engineering'),
            ('S004', 'Sneha Deshmukh', 'B.Tech in Electronics & Communication Engineering'),
            ('S005', 'Pranav Shinde', 'B.Tech in Chemical Engineering'),
            ('S006', 'Tanvi Joshi', 'M.Tech (Various specializations)'),
            ('S007', 'Mihir Pawar', 'B.Tech in Computer Science & Engineering'),
            ('S008', 'Kavya Gokhale', 'B.Tech in Artificial Intelligence & Data Science'),
            ('S009', 'Aditya More', 'B.Tech in Cybersecurity'),
            ('S010', 'Neha Bhosale', 'B.Tech in Robotics & Automation'),
            ('S011', 'Yash Khandekar', 'M.Tech in Computer Science'),
            ('S012', 'Isha Gaikwad', 'MCA (Master of Computer Applications)'),
            ('S013', 'Soham Kale', 'Diploma in Mechanical Engineering'),
            ('S014', 'Prachi Desai', 'Diploma in Civil Engineering'),
            ('S015', 'Nikhil Salunkhe', 'Diploma in Computer Engineering'),
            ('S016', 'Anaya Chavan', 'Diploma in Electrical Engineering'),
            ('S017', 'Rohan Jagtap', 'Diploma in Electronics & Telecommunication'),
            ('S018', 'Shreya Apte', 'BBA (General)'),
            ('S019', 'Kunal Pawar', 'BBA (International Business)'),
            ('S020', 'Meera Dixit', 'BBA (Marketing / Finance / HR)'),
            ('S021', 'Varun Phadnis', 'MBA (Various specializations)'),
            ('S022', 'Aishwarya Kulkarni', 'MBA (Various specializations)'),
            ('S023', 'Tejas Mane', 'B.Com (General)'),
            ('S024', 'Smita Karve', 'B.Com (International Accounting & Finance)'),
            ('S025', 'Arnav Inamdar', 'B.A. (Hons) Economics'),
            ('S026', 'Rutuja Wagh', 'M.Com'),
            ('S027', 'Harshavardhan Patil', 'M.A. Economics'),
            ('S028', 'Pooja Nikam', 'B.Tech in Petroleum Engineering'),
            ('S029', 'Siddharth Sawant', 'M.Tech (Various specializations)'),
            ('S030', 'Gayatri Kapse', 'MCA (Master of Computer Applications)'),
        ]
        
        created_count = 0
        
        for student_id, student_name, program_name in students_data:
            # Skip if student already exists
            if Student.objects.filter(registration_number=student_id).exists():
                continue
                
            # Find program
            program = Program.objects.filter(name=program_name).first()
            if not program:
                self.stdout.write(f'  ❌ Program not found: {program_name}')
                continue
            
            # Create username
            username = student_name.lower().replace(' ', '_')
            
            # Create user
            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': student_name.split()[0],
                    'last_name': ' '.join(student_name.split()[1:]),
                    'email': f'{username}@college.edu',
                }
            )
            
            if user_created:
                user.set_password('student123')
                user.save()
            
            # Create student
            Student.objects.create(
                user=user,
                registration_number=student_id,
                name=student_name,
                email=f'{username}@college.edu',
                phone=f'9876{student_id[1:4]}000',
                program=program,
                admission_date=date(2024, 7, 1),
                current_semester=1,
                is_active=True
            )
            
            created_count += 1
            self.stdout.write(f'  ✅ Created: {student_name} ({student_id}) - {program.code}')
        
        self.stdout.write(f'\n📊 Summary: Created {created_count} students')
        self.stdout.write('🔑 Default password for all students: student123')