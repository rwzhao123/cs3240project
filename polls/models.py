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
from django_extensions.db import models as dj_extensions_models




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

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE, related_name='profile')
    student_first_name = models.CharField(max_length=200, blank = True)
    student_last_name = models.CharField(max_length=200, blank = True)
    student_email = models.CharField(max_length=200, blank = True)
    student_tutor = models.BooleanField(default=False)
    skills = models.CharField(max_length=200, blank = True)
    availability = models.CharField(max_length=200, blank = True)



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




    def __str__(self):
        return self.student_last_name


    def is_upperclass(self):
        return self.student_year_in_school in {self.THIRD_YEAR, self.FOURTH_YEAR}
    def is_tutor(self):
        return self.student_tutor
    @receiver(post_save,sender = User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Student.objects.create(user =instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        instance.profile.save()


class ChatMessage(dj_extensions_models.TimeStampedModel):
    username = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()


class UserEvent(dj_extensions_models.TimeStampedModel):
    user_name = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()



