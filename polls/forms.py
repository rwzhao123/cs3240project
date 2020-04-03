from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Student
from django import forms

#class UserForm(forms.ModelForm):
    #class Meta:
        #model = Student
        #fields = ('student_first_name', 'student_last_name', 'student_email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('student_year_in_school', 'skills', 'availability', 'student_tutor')

#class ChoiceForm(forms.ModelForm):
    #class Meta:
        #model = Student
        #fields = ('student_tutor',)
        # student_tutor = forms.ChoiceField(widget=forms.RadioSelect, choices=TUTOR_CHOICES)
