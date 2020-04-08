from django.db import models
import datetime
# Create your models here.
from django.db import models
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

        was_published_recently.admin_order_field = 'pub_date'
        was_published_recently.boolean = True
        was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


class Suggestion(models.Model):
    name_text = models.CharField(max_length=200)
    suggestion_text = models.TextField()
    def __str__(self):
        return self.name_text



class Student(models.Model):

    user = models.OneToOneField(User, unique=True, null=True, db_index=True, on_delete=models.CASCADE, related_name='profile')
    preferred_name = models.CharField(max_length=200, default="Name")
    student_tutor = models.BooleanField(default=False)
    need_help_with = models.CharField(max_length=200, blank = True)
    skills = models.CharField(max_length=200, blank = True)
    availability = models.CharField(max_length=200, blank = True)
    location = models.CharField(max_length=200, default="Somewhere")
    
    requested = models.ManyToManyField(User, blank=True)



    FIRST_YEAR= '1Y'
    SECOND_YEAR = '2Y'
    THIRD_YEAR = '3Y'
    FOURTH_YEAR = '4Y'
    GRADUATE = 'GR'
    YEAR_IN_SCHOOL_CHOICES = [
        (FIRST_YEAR, 'First Year'),
        (SECOND_YEAR, 'Second Year'),
        (THIRD_YEAR, 'Third Year'),
        (FOURTH_YEAR, 'Fourth Year'),
        (GRADUATE, 'Graduate'),
    ]
    student_year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FIRST_YEAR,)




    #def __str__(self):
        #return self.student_last_name


    def is_upperclass(self):
        return self.student_year_in_school in {self.THIRD_YEAR, self.FOURTH_YEAR}
    def is_tutor(self):
        return self.student_tutor




    @receiver(post_save,sender = User)
    def create_user_profile(sender, instance, created, **kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            s = Student(user = instance)
            s.save()
        print("user created")
        if created:
            s = Student(user = instance)
            s.save()
            print(created)
            Student.objects.create(user =instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        instance.profile.save()


class TutorRequest(models.Model):
    subject = models.CharField(max_length = 200)
    subject_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    in_progress = models.BooleanField(default= False)
    student = models.ForeignKey(Student, on_delete = models.CASCADE)














