from django.core.management.base import BaseCommand
from app.models import Department, Program

class Command(BaseCommand):
    help = 'Load initial data for departments and programs'

    def handle(self, *args, **options):
        self.stdout.write('Loading departments and programs...')
        
        # Department data with their programs
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

        # Create departments and programs
        for dept_data in departments_data:
            # Create or get department
            department, created = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults={'name': dept_data['name']}
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created department: {department.name}')
                )
            else:
                self.stdout.write(f'Department already exists: {department.name}')
            
            # Create programs for this department
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
                    self.stdout.write(
                        self.style.SUCCESS(f'  Created program: {program.name}')
                    )
                else:
                    self.stdout.write(f'  Program already exists: {program.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded all departments and programs!')
        )