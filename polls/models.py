from django.db import models
import datetime
# Create your models here.
from django.db import models
from django.utils import timezone
from django import forms



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
    student_first_name = models.CharField(max_length=200)
    student_last_name = models.CharField(max_length=200)
    student_email = models.CharField(max_length=200)




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
        default=FIRST_YEAR,
    )

    def is_upperclass(self):
        return self.student_year_in_school in {self.THIRD_YEAR, self.FOURTH_YEAR}

class Tutor(models.Model):
    tutor_first_name = models.CharField(label = "First Name")
    tutor_last_name = models.CharField(label = "Last Name")
    tutor_email = models.CharField(label = "Email")
    tutor_skills = models.CharField(label = "Skills")
    tutor_availability = models.CharField(label = "Availability")

class UpdateTutorProfile(forms.ModelForm):
    username = forms.CharField()
    email = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    skills = forms.CharField()
    availability = forms.CharField()

    class Meta:
        model = Tutor
        fields = ('tutor_first_name', 'tutor_email', 'tutor_last_name', 'skills', 'availability')

    def change_fields(self):
        availability = self.clean_data.get('availiability')
        skills = self.clean_data.get('skills')

    def save(self, commit = True):
        user = super(RegistrationForm, self).save(commit=False) # look at this again
        user.availability = self.clean_data.get('availability')
        user.skills = self.clean_data.get('skills')
        if commit:
            user.save()
        return user
