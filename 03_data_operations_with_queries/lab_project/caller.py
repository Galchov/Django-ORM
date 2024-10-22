import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import (
    Student,
    Employee
)


# Run and print your queries
def add_students():
    # Option 1 (Preferred way of adding objects):
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com'
    )

    # Option 2:
    student = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        birth_date=None,  # Or just ignore that field
        email='jane.smith@university.com',
    )
    student.save()

    # Option 3:
    student = Student()
    student.student_id = 'FH2014'
    student.first_name = 'Alice'
    student.last_name = 'Johnson'
    student.birth_date = '1998-02-10'
    student.email = 'alice.johnson@university.com'
    student.save()

    Student.objects.create(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com',
    )


def get_students_info():
    students = Student.objects.all()
    students_info = []

    for stud in students:
        students_info.append(f"Student №{stud.student_id}: "
                             f"{stud.first_name} "
                             f"{stud.last_name}; "
                             f"Email: {stud.email}")

    return '\n'.join(students_info)


def update_students_emails():
    students = Student.objects.all()

    for stud in students:
        stud.email = stud.email.replace(stud.email.split('@')[1], 'uni-students.com')
        stud.save()


def truncate_students():
    students = Student.objects.all()
    students.delete()


# Employee model examples:
def get_all_engineers():
    engineers = Employee.objects.filter(department='Engineering')
    result = []

    for e in engineers:
        result.append(f"{e.first_name} "
                      f"{e.last_name} from "
                      f"{e.department} working as "
                      f"{e.position}")

    return '\n'.join(result)


def get_all_managers():
    all_employees = Employee.objects.all()
    managers = []

    for e in all_employees:
        position_info = e.position.split()
        if 'Manager' in position_info:
            managers.append(f"{e.first_name}, manager of {e.department}")

    return '\n'.join(managers)


# Run queries

# add_students()
# print(Student.objects.all())

# print(get_students_info())

# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)

# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")

# print(get_all_engineers())

# print(get_all_managers())
