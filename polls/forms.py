from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Student, TutorRequest
from django import forms


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('preferred_name', 'student_year_in_school', 'student_tutor', 'bio', 'venmo')

    def save(self, commit= True):
        student = super(ProfileForm, self).save(commit=True)
        student.preferred_name = self.cleaned_data['preferred_name']
        student.student_year_in_school = self.cleaned_data['student_year_in_school']
        student.student_tutor = self.cleaned_data['student_tutor']
        student.venmo = self.cleaned_data['venmo']
        student.bio = self.cleaned_data['bio']
        if commit:
            student.save()
        return student



    

