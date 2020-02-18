from django.test import TestCase
from polls.models import Student

class StudentTestCase(TestCase):
    def setUp(self):
        Student.objects.create(student_first_name="Brenna", student_last_name="McGowan", student_email="mcgowan.brennan@gmail.com")
