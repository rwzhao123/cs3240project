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
    #requested=forms.ModelMultipleChoiceField(queryset=User.objects.all()[:2])
    class Meta:
        model = Student
        fields = ('preferred_name', 'student_year_in_school', 'need_help_with', 'location', 'availability', 'student_tutor', 'skills', 'venmo')

    def save(self, commit= True):
        student = super(ProfileForm, self).save(commit=True)
        student.preferred_name = self.cleaned_data['preferred_name']
        student.student_year_in_school = self.cleaned_data['student_year_in_school']
        student.need_help_with = self.cleaned_data['need_help_with']
        student.availability = self.cleaned_data['availability']
        student.student_tutor = self.cleaned_data['student_tutor']
        student.location = self.cleaned_data['location']
        student.venmo = self.cleaned_data['venmo']
        if commit:
            student.save()
        return student

# form to make requesting work
class RequestForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('requested',)
        requests = {'requests': forms.HiddenInput()}

    #requested = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    def __init__(self, *args, **kwargs):
        assert 'initial' in kwargs and 'requests' in kwargs['initial'] and type(kwargs['initial']['requests'] is User)
        super(RequestForm, self).__init__(*args, **kwargs)
        requests = kwargs['initial']['requests']
        self.fields['requested'].queryset = User.objects.filter(requests=requests)


    

class TutorForm(forms.ModelForm):
    class Meta:
        model= TutorRequest
        fields={'tutor','student', 'subject','subject_text', 'contact_info'}
    def save(self, commit=True):
        tutor_request = super(TutorForm, self).save(commit=True)
        tutor_request.tutor = self.cleaned_data['tutor']
        tutor_request.student=self.cleaned_data['student']
        tutor_request.subject=self.cleaned_data['subject']
        tutor_request.subject_text=self.cleaned_data['subject_text']
        tutor_request.contact_info = self.cleaned_data['contact_info']
        if commit:
            tutor_request.save()
        return tutor_request


# class RequestForm(forms.ModelForm):
#     class Meta:
#         model = TutorRequest
#         fields = ('subject','subject_text', 'pub_date')
#     def save(self, commit=True):
#         tr = super(RequestForm,self).save(commit=False)
#         tr.subject = self.clean_data['subject']
#         tr.subject_text = self.clean_data['subject_text']
#         if commit:
#             tr.save()
#         return tr



#class ChoiceForm(forms.ModelForm):
    #class Meta:
        #model = Student
        #fields = ('student_tutor',)
        # student_tutor = forms.ChoiceField(widget=forms.RadioSelect, choices=TUTOR_CHOICES)
