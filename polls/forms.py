from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Student, TutorRequest
from django import forms

#class UserForm(forms.ModelForm):
    #class Meta:
        #model = Student
        #fields = ('student_first_name', 'student_last_name', 'student_email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('student_year_in_school', 'skills', 'availability', 'student_tutor')

    def save(self, commit= True):
        student = super(ProfileForm, self).save(commit=False)
        student.student_year_in_school = self.cleaned_data['student_year_in_school']
        student.skills = self.cleaned_data['skills']
        student.availability = self.cleaned_data['availability']
        student.student_tutor = self.cleaned_data['student_tutor']
        if commit:
            student.save()
        return student


class RequestForm(forms.ModelForm):
    class Meta:
        model = TutorRequest
        fields = ('subject','subject_text', 'pub_date')
    def save(self, commit=True):
        tr = super(RequestForm,self).save(commit=False)
        tr.subject = self.clean_data['subject']
        tr.subject_text = self.clean_data['subject_text']
        if commit:
            tr.save()
        return tr



#class ChoiceForm(forms.ModelForm):
    #class Meta:
        #model = Student
        #fields = ('student_tutor',)
        # student_tutor = forms.ChoiceField(widget=forms.RadioSelect, choices=TUTOR_CHOICES)
