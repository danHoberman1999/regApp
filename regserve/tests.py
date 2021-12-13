from django.test import TestCase, Client
from .models import *
import io
from rest_framework.parsers import JSONParser
from .serializers import *

class DataTest(TestCase):
    def setUp(self):
        Student.objects.create(
            firstname="First",
            lastname="Student",
            idnumber=100,
            email="student.first@school.edu",
            schoolyear="FR",
            major="CS",
            gpa="4.0"
        )

        Student.objects.create(
            firstname="Second",
            lastname="Student",
            idnumber=101,
            email="student.second@school.edu",
            schoolyear="SR",
            major="ENG",
            gpa="3.0"
        )

        self.test_client = Client()

    # Test cases for the REST API
    def test_student_api(self):
        students_response = self.test_client.get('/regserve/data/students/')
        print(f'STUDENT API TEST - inside test, response is:\n{students_response}\n\
            and status code is:\n{students_response.status_code}\n')
        self.assertEqual(students_response.status_code, 200)

        print(f'STUDENT API TEST - inside test, response content is:\n\
            {students_response.content} \n')
        student_stream = io.BytesIO(students_response.content)
        print(f'STUDENT API TEST - inside test, student stream is:\n\
            {student_stream}\n')
        student_api_data = JSONParser().parse(stream=student_stream)
        print(f'STUDENT API TEST - inside test, student api data is:\n\
            {student_api_data}\n')
        first_student_data = student_api_data[0]
        print(f'STUDENT API TEST - inside test, first student data is:\n\
            {first_student_data} \n and id is {first_student_data["id"]}\n')
        first_student_db = Student.objects.get(id=first_student_data['id'])
        print(f'STUDENT API TEST - inside test, first student DB is: \n\
            {first_student_db} \n')
        first_student_serializer = StudentSerializer(first_student_db,
            data=first_student_data)
        print(f'STUDENT API TEST - inside test, first student serializer is:\n\
            {first_student_serializer}\n')
        print(f'STUDENT API TEST - inside test, first student serializer valid is:\n\
            {first_student_serializer.is_valid()}')
        first_student_api = first_student_serializer.save()
        print(f'STUDENT API TEST - inside test, first student API is:\n\
            {first_student_api}\n')
        self.assertEqual(first_student_api, first_student_db)


    # Test assertions for studetn
    def test_student(self):
        student_list = Student.objects.all()
        for student in student_list:
            print(f'inside Student, current Student is {student}\n')
        student = student_list[0]
        self.assertEqual(student.id, 1)
        self.assertEqual(student.full_name, "First Student")
        self.assertEqual(student.idnumber, 100)
        self.assertEqual(student.schoolyear, 'FR')
        self.assertEqual(student.major, "CS")
        self.assertEqual(student.gpa, 4.0)

class SimpleTest(TestCase):
    # need to run this everytime before test
    def setUp(self):
        self.test_client = Client()

    # test case for the hello world regserve page
    def test_response(self):
        response = self.test_client.get('/regserve')
        print(f'Inside HelloWorld test, response is {response}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello from django backend')
        