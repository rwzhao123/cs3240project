from django.db import models
import datetime
# Create your models here.
from django.db import models
from django.utils import timezone


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



from ratings.handlers import ratings
from ratings.forms import SliderVoteForm
ratings.register(Tutor, score_range=(1, 10), form_class=SliderVoteForm)
