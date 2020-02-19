from django.test import TestCase
from django.urls import reverse
from django.views import generic
from polls.models import Student

class StudentModelTests(TestCase):
    def setUp(self):
        Student.objects.create(student_first_name="Brennan", student_last_name="McGowan", student_email="mcgowan.brennan@gmail.com")
