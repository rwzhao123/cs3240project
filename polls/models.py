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
    user = models.OneToOneField(User, unique=True, null=True, db_index=True, on_delete=models.CASCADE,
                                related_name='profile')
    preferred_name = models.CharField(max_length=200, default="Name")
    student_tutor = models.BooleanField(default=False)
    bio = models.CharField(max_length=200, blank=True)
    available = models.BooleanField(default=False)
    tutor_notifications = models.IntegerField(default=0)
    student_notifications = models.IntegerField(default=0)
    venmo = models.CharField(max_length=200, default = "")

    FIRST_YEAR = '1Y'
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
        default=FIRST_YEAR, )

    def __str__(self):
        return self.user.username

    def is_upperclass(self):
        return self.student_year_in_school in {self.THIRD_YEAR, self.FOURTH_YEAR}

    def is_tutor(self):
        return self.student_tutor

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            s = Student(user=instance)
            s.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        instance.profile.save()

    def add_notification(self, tutor=False):
        if tutor:
            self.tutor_notifications += 1
        else:
            self.student_notifications += 1
        self.save()

    def reset_notification(self, tutor=False):
        if tutor:
            self.tutor_notifications = 0
        else:
            self.student_notifications = 0
        self.save()

    def change_availability(self):
        self.available = not self.available
        self.save()


class TutorRequest(models.Model):
    tutor = models.ForeignKey(Student, related_name='requested_tutor', on_delete=models.CASCADE, default=1)
    student = models.ForeignKey(Student, related_name='student_requester', on_delete=models.CASCADE, default=1)
    subject = models.CharField(max_length=200, default="")
    subject_text = models.TextField(default="")
    modified_date = models.DateTimeField(default=timezone.now())
    contact_info = models.CharField(max_length=200, default="")
    location = models.CharField(max_length=200, default="")
    archived_tutor = models.BooleanField(default=False)
    archived_student = models.BooleanField(default=False)

    PROGRESS = [(1, 'PENDING'),
                (2, 'CANCELED'),
                (3, 'ACCEPTED'),
                (4, 'DECLINED'),
                (5, 'COMPLETED')]

    progress = models.IntegerField(choices=PROGRESS, default=1)
    def update_request(self, progress_update):
        self.progress = progress_update
        self.modified_date = timezone.now()
        self.save()



    def configure_url(self):

        CHAT_URL = "https://chat-site6.herokuapp.com/"
        new_url = CHAT_URL + "chat-room-" + str(self.id)
        return new_url

    def is_old(self):
        now = timezone.now()
        return not (now - datetime.timedelta(days=1) <= self.pub_date <= now)

    def archive(self, tutor=False):
        if tutor:
            self.archived_tutor = True
        else:
            self.archived_student = True
        self.save()

