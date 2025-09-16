from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Department, Program, Student
from datetime import date

class Command(BaseCommand):
    help = 'Load initial student data'

    def handle(self, *args, **options):
        self.stdout.write('Loading student data...')
        
        # Student data
        students_data = [
            ('S001', 'Aarav Patil', 'School of Engineering & Technology', 'B.Tech in Civil Engineering'),
            ('S002', 'Riya Kulkarni', 'School of Engineering & Technology', 'B.Tech in Mechanical Engineering'),
            ('S003', 'Omkar Jadhav', 'School of Engineering & Technology', 'B.Tech in Electrical & Electronics Engineering'),
            ('S004', 'Sneha Deshmukh', 'School of Engineering & Technology', 'B.Tech in Electronics & Communication Engineering'),
            ('S005', 'Pranav Shinde', 'School of Engineering & Technology', 'B.Tech in Chemical Engineering'),
            ('S006', 'Tanvi Joshi', 'School of Engineering & Technology', 'M.Tech (Various specializations)'),
            ('S007', 'Mihir Pawar', 'School of Computer Science & Engineering', 'B.Tech in Computer Science & Engineering'),
            ('S008', 'Kavya Gokhale', 'School of Computer Science & Engineering', 'B.Tech in Artificial Intelligence & Data Science'),
            ('S009', 'Aditya More', 'School of Computer Science & Engineering', 'B.Tech in Cybersecurity'),
            ('S010', 'Neha Bhosale', 'School of Computer Science & Engineering', 'B.Tech in Robotics & Automation'),
            ('S011', 'Yash Khandekar', 'School of Computer Science & Engineering', 'M.Tech in Computer Science'),
            ('S012', 'Isha Gaikwad', 'School of Computer Science & Engineering', 'MCA (Master of Computer Applications)'),
            ('S013', 'Soham Kale', 'School of Polytechnic', 'Diploma in Mechanical Engineering'),
            ('S014', 'Prachi Desai', 'School of Polytechnic', 'Diploma in Civil Engineering'),
            ('S015', 'Nikhil Salunkhe', 'School of Polytechnic', 'Diploma in Computer Engineering'),
            ('S016', 'Anaya Chavan', 'School of Polytechnic', 'Diploma in Electrical Engineering'),
            ('S017', 'Rohan Jagtap', 'School of Polytechnic', 'Diploma in Electronics & Telecommunication'),
            ('S018', 'Shreya Apte', 'School of Management', 'BBA (General)'),
            ('S019', 'Kunal Pawar', 'School of Management', 'BBA (International Business)'),
            ('S020', 'Meera Dixit', 'School of Management', 'BBA (Marketing / Finance / HR)'),
            ('S021', 'Varun Phadnis', 'School of Management', 'MBA (Various specializations)'),
            ('S022', 'Aishwarya Kulkarni', 'School of Management', 'MBA (Various specializations)'),
            ('S023', 'Tejas Mane', 'School of Economics & Commerce', 'B.Com (General)'),
            ('S024', 'Smita Karve', 'School of Economics & Commerce', 'B.Com (International Accounting & Finance)'),
            ('S025', 'Arnav Inamdar', 'School of Economics & Commerce', 'B.A. (Hons) Economics'),
            ('S026', 'Rutuja Wagh', 'School of Economics & Commerce', 'M.Com'),
            ('S027', 'Harshavardhan Patil', 'School of Economics & Commerce', 'M.A. Economics'),
            ('S028', 'Pooja Nikam', 'School of Engineering & Technology', 'B.Tech in Petroleum Engineering'),
            ('S029', 'Siddharth Sawant', 'School of Engineering & Technology', 'M.Tech (Various specializations)'),
            ('S030', 'Gayatri Kapse', 'School of Computer Science & Engineering', 'MCA (Master of Computer Applications)'),
        ]
        
        created_count = 0
        existing_count = 0
        
        for student_id, student_name, dept_name, program_name in students_data:
            try:
                # Find the program
                program = Program.objects.filter(name=program_name).first()
                if not program:
                    # Try to find by partial match for similar programs
                    program = Program.objects.filter(name__icontains=program_name.split()[0]).first()
                    if not program:
                        self.stdout.write(
                            self.style.ERROR(f'Program not found for {student_name}: {program_name}')
                        )
                        continue
                
                # Check if student already exists
                if Student.objects.filter(registration_number=student_id).exists():
                    existing_count += 1
                    self.stdout.write(f'Student already exists: {student_name} ({student_id})')
                    continue
                
                # Create username from student name (lowercase, no spaces)
                username = student_name.lower().replace(' ', '_')
                
                # Create or get user
                user, user_created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': student_name.split()[0],
                        'last_name': ' '.join(student_name.split()[1:]),
                        'email': f'{username}@college.edu',
                    }
                )
                
                if user_created:
                    user.set_password('student123')  # Default password
                    user.save()
                
                # Create student
                student = Student.objects.create(
                    user=user,
                    registration_number=student_id,
                    name=student_name,
                    email=f'{username}@college.edu',
                    phone=f'9876{student_id[1:4]}000',  # Generate sample phone number
                    program=program,
                    admission_date=date(2024, 7, 1),  # Sample admission date
                    current_semester=1,
                    is_active=True
                )
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created student: {student_name} ({student_id}) - {program.name}'
                    )
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating student {student_name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Student data loading completed!\n'
                f'Created: {created_count} students\n'
                f'Already existed: {existing_count} students\n'
                f'Default password for all students: student123'
            )
        )