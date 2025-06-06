import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Student


def add_students():
    # Preferred method for creating a DB record
    Student.objects.create(
        student_id="FC5204",
        first_name="John",
        last_name="Doe",
        birth_date="1995-05-15",
        email = "john.doe@university.com"
    )

    # Option 2 (Not preferred)
    student = Student(
        student_id="FE0054",
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@university.com"
    )
    student.save()

    # Option 3 (Not preferred)
    student = Student()
    student.student_id = "FH2014"
    student.first_name = "Alice"
    student.last_name = "Johnson"
    student.birth_date = "1998-02-10"
    student.email = "alice.johnson@university.com"
    student.save()

    Student.objects.create(
        student_id="FH2015",
        first_name="Bob",
        last_name="Wilson",
        birth_date="1996-11-25",
        email="bob.wilson@university.com"
    )


def get_students_info():
    all_students = Student.objects.all()
    students_info = []

    for s in all_students:
        students_info.append(f"Student №{s.student_id}: {s.first_name} {s.last_name}; Email: {s.email}")
    
    return '\n'.join(students_info)


def update_students_emails():
    all_students = Student.objects.all()

    for s in all_students:
        s.email = s.email.replace(s.email.split('@')[1], 'uni-students.com')
        s.save()


def truncate_students():
    Student.objects.all().delete()

# Task 1:
# add_students()
# print(Student.objects.all())

# Task 2:
# print(get_students_info())

# Task 3:
# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)

# Task 4:
# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")
