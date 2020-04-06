
from django.test import TestCase
from polls.models import Student
#views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django.test import TestCase



#class TestSuite(TestCase):
   # def setUp(self):
        #user = User.objects.create_user(
            #username='jacob', email='jacob@gmail.com', password='top_secret')

    #def test_user_can_login(self):
        #response = self.client.post("/login", {"username": "jacob", "password": "top_secret"})



class HomePageTests(TestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 404)


class StudentTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='brennan', email='test@gmail.com', password='top_secret')
        Student.objects.create(user=user, student_first_name='brennan', student_last_name='mcgowan',
                               student_email='test@gmail.com',
                               student_tutor=False, skills='None', availability='None')
        user2 = User.objects.create_user(
            username='michael', email='test2@gmail.com', password='top_secret')
        Student.objects.create(user=user2, student_first_name='michael', student_last_name='ferguson',
                               student_email='test@gmail.com',
                               student_tutor=True, skills='None', availability='None')


def test_student(self):
    stud = Student.objects.get(username='brennan')
    expected_object_name = f'{stud.student_last_name}'
    self.assertEquals(expected_object_name, 'mcgowan')
    stud2 = Student.objects.get(username='brennan')
    is_tutor = f'{stud2.student_tutor}'
    is_tutor2 = f'{stud.student_tutor}'
    self.assertEquals(is_tutor, True)
    self.assertEquals(is_tutor2, False)
