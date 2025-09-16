from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Department, Teacher
from datetime import date

class Command(BaseCommand):
    help = 'Load initial faculty/teacher data'

    def handle(self, *args, **options):
        self.stdout.write('Loading faculty data...')
        
        # Faculty data with realistic Indian names and qualifications
        faculty_data = [
            # School of Engineering & Technology
            ('T001', 'Dr. Rajesh Kumar', 'SET', 'professor', 'Ph.D. in Civil Engineering', 'Structural Engineering', 15, date(2010, 8, 1)),
            ('T002', 'Dr. Priya Sharma', 'SET', 'associate_professor', 'Ph.D. in Mechanical Engineering', 'Thermal Engineering', 12, date(2012, 7, 15)),
            ('T003', 'Dr. Vikram Singh', 'SET', 'professor', 'Ph.D. in Electrical Engineering', 'Power Systems', 18, date(2008, 6, 10)),
            ('T004', 'Prof. Sunita Patel', 'SET', 'assistant_professor', 'M.Tech in Electronics Engineering', 'Communication Systems', 8, date(2016, 8, 20)),
            ('T005', 'Dr. Arun Desai', 'SET', 'associate_professor', 'Ph.D. in Chemical Engineering', 'Process Engineering', 10, date(2014, 7, 5)),
            ('T006', 'Dr. Kavita Joshi', 'SET', 'professor', 'Ph.D. in Petroleum Engineering', 'Reservoir Engineering', 16, date(2009, 9, 1)),
            
            # School of Computer Science & Engineering  
            ('T007', 'Dr. Amit Agarwal', 'SCSE', 'hod', 'Ph.D. in Computer Science', 'Artificial Intelligence', 20, date(2005, 7, 1)),
            ('T008', 'Prof. Neha Gupta', 'SCSE', 'associate_professor', 'Ph.D. in Data Science', 'Machine Learning', 9, date(2015, 8, 15)),
            ('T009', 'Dr. Rohit Malhotra', 'SCSE', 'professor', 'Ph.D. in Cybersecurity', 'Network Security', 14, date(2011, 6, 20)),
            ('T010', 'Prof. Anjali Verma', 'SCSE', 'assistant_professor', 'M.Tech in Robotics', 'Automation Systems', 6, date(2018, 7, 10)),
            ('T011', 'Dr. Karan Mehta', 'SCSE', 'associate_professor', 'Ph.D. in Computer Science', 'Software Engineering', 11, date(2013, 8, 5)),
            
            # School of Polytechnic
            ('T012', 'Prof. Ramesh Yadav', 'SOP', 'hod', 'M.Tech in Mechanical Engineering', 'Manufacturing Technology', 22, date(2002, 9, 1)),
            ('T013', 'Prof. Seema Thakur', 'SOP', 'associate_professor', 'M.Tech in Civil Engineering', 'Construction Technology', 13, date(2011, 7, 15)),
            ('T014', 'Prof. Manoj Kumar', 'SOP', 'assistant_professor', 'M.Tech in Computer Engineering', 'Programming & Databases', 7, date(2017, 8, 20)),
            ('T015', 'Prof. Ritu Saxena', 'SOP', 'lecturer', 'M.Tech in Electrical Engineering', 'Power Electronics', 5, date(2019, 7, 10)),
            
            # School of Management
            ('T016', 'Dr. Suresh Agrawal', 'SOM', 'professor', 'Ph.D. in Management', 'Strategic Management', 17, date(2008, 8, 1)),
            ('T017', 'Prof. Pooja Srivastava', 'SOM', 'associate_professor', 'MBA, Ph.D. in Finance', 'Financial Management', 10, date(2014, 7, 15)),
            ('T018', 'Prof. Deepak Tiwari', 'SOM', 'assistant_professor', 'MBA in Marketing', 'Digital Marketing', 8, date(2016, 6, 20)),
            ('T019', 'Dr. Meera Chopra', 'SOM', 'associate_professor', 'Ph.D. in Human Resources', 'Organizational Behavior', 12, date(2012, 9, 5)),
            
            # School of Economics & Commerce
            ('T020', 'Dr. Ashok Pandey', 'SEC', 'hod', 'Ph.D. in Economics', 'Development Economics', 19, date(2006, 7, 1)),
            ('T021', 'Prof. Shilpa Jain', 'SEC', 'associate_professor', 'M.Com, Ph.D. in Commerce', 'International Trade', 11, date(2013, 8, 15)),
            ('T022', 'Dr. Vijay Sharma', 'SEC', 'professor', 'Ph.D. in Economics', 'Econometrics', 15, date(2010, 6, 10)),
            ('T023', 'Prof. Anita Singh', 'SEC', 'assistant_professor', 'M.Com, CA', 'Accounting & Finance', 9, date(2015, 7, 20)),
        ]
        
        created_count = 0
        existing_count = 0
        
        for emp_id, name, dept_code, designation, qualification, specialization, experience, joining_date in faculty_data:
            try:
                # Find department
                department = Department.objects.filter(code=dept_code).first()
                if not department:
                    self.stdout.write(
                        self.style.ERROR(f'Department not found: {dept_code}')
                    )
                    continue
                
                # Check if teacher already exists
                if Teacher.objects.filter(employee_id=emp_id).exists():
                    existing_count += 1
                    self.stdout.write(f'Teacher already exists: {name} ({emp_id})')
                    continue
                
                # Create username from teacher name
                username = name.lower().replace('dr. ', '').replace('prof. ', '').replace(' ', '_')
                
                # Create or get user
                user, user_created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': name.split()[-2] if len(name.split()) > 2 else name.split()[0],
                        'last_name': name.split()[-1],
                        'email': f'{username}@college.edu',
                        'is_staff': True,  # Teachers should have staff access
                    }
                )
                
                if user_created:
                    user.set_password('teacher123')  # Default password
                    user.save()
                
                # Create teacher
                teacher = Teacher.objects.create(
                    user=user,
                    employee_id=emp_id,
                    name=name,
                    email=f'{username}@college.edu',
                    phone=f'9876{emp_id[1:4]}111',  # Generate sample phone number
                    department=department,
                    designation=designation,
                    qualification=qualification,
                    specialization=specialization,
                    experience_years=experience,
                    is_active=True,
                    joining_date=joining_date
                )
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created teacher: {name} ({emp_id}) - {department.name}'
                    )
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating teacher {name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Faculty data loading completed!\n'
                f'Created: {created_count} teachers\n'
                f'Already existed: {existing_count} teachers\n'
                f'Default password for all teachers: teacher123'
            )
        )