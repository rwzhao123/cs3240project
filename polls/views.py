from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from .models import Student, TutorRequest

from .forms import ProfileForm


# home page views

def index(request):
    return render(request, "polls/new_index.html")


def chat(request):
    return render(request, 'polls/chat.html')


def room(request, room_name):
    return render(request, 'polls/room.html', {
        'room_name': room_name
    })


# profile view functions

def student_profile(request):
    return render(request, "polls/new_edit_profile.html")


@login_required
def update_profile(request):
    print("this was called")
    return render(request, "polls/new_profile.html")


@login_required
def edit_info(request):
    if request.method == "POST":
        print("in here")
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect("/quick-tutor/student_profile")
    else:

        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, "polls/new_edit_profile.html", {"profile_form": profile_form})


# website details
def about(request):
    return render(request, "polls/about.html")


def contact_us(request):
    return render(request, "polls/contact_us.html")


# tutor matching views

def confirm_match(request):
    return render(request, "polls/new_confirm_match.html")


def error_match(request):
    return render(request, "polls/error_match.html")


def confirm_cancel(request):
    return render(request, "polls/new_confirm_cancel.html")


def become_available(request):
    Student.objects.get(user=request.user).change_availability()
    return render(request, "polls/new_profile.html")


def student_requests(request):
    student = Student.objects.get(user=request.user)
    args = format_requests(student)
    return render(request, "polls/new_student_page.html", args)


def tutor_requests(request):
    tutor = Student.objects.get(user=request.user)
    args = format_requests(tutor, True)
    return render(request, "polls/new_tutor_page.html", args)


def format_requests(user, tutor=False):
    if tutor:
        requests = TutorRequest.objects.filter(tutor=user).exclude(archived_tutor=True).order_by('-modified_date')
        notifs = user.tutor_notifications
    else:
        requests = TutorRequest.objects.filter(student=user).exclude(archived_student=True).order_by('-modified_date')
        notifs = user.student_notifications

    user.reset_notification(tutor)

    args = {'requests': requests, 'notifs': notifs}
    return args


def create_request(request, student_id):
    requested_user = User.objects.get(id=student_id)
    tutor_requested = Student.objects.get(user=requested_user)
    student_requester = Student.objects.get(user=request.user)
    tutor_requested.add_notification(True)
    student_requester.add_notification()
    tr = TutorRequest.objects.create(student=student_requester, tutor=tutor_requested, modified_date=timezone.now())
    tr.subject = request.POST['tutor_subject']
    tr.subject_text = request.POST['tutor_additional']
    tr.contact_info = request.POST['contact_method']
    tr.location = request.POST['location']
    tutor_requested.save()
    student_requester.save()
    tr.save()
    return redirect('quick-tutor:confirm')


class AllStudentsView(generic.ListView):
    student_list = Student.objects.all()
    template_name = 'polls/new_tutor_match.html'

    def get_queryset(self):
        return Student.objects.filter(available=True)


def additional_info(request, student_id):
    tutor = Student.objects.get(id=student_id)
    return render(request, 'polls/new_additional_info.html', {'tutor': tutor, 'tutor_id': student_id})


def student_cancel(request, t_request_id):
    canceled_request = TutorRequest.objects.get(id=t_request_id)
    tutor = canceled_request.tutor
    canceled_request.update_request(2)
    tutor.add_notification()
    canceled_request.save()
    tutor.save()
    return redirect("quick-tutor:confirm_cancel")


# functions implementing actions on requests

def tutor_decline(request, s_request_id):
    tentative_request = TutorRequest.objects.get(id=s_request_id)
    student = tentative_request.student
    student.add_notification()
    tentative_request.update_request(4)
    tentative_request.save()
    student.save()
    return render(request, "polls/confirm_update.html", {'status': "Declined"})


def tutor_accept(request, s_request_id):
    tentative_request = TutorRequest.objects.get(id=s_request_id)
    student = tentative_request.student
    tentative_request.update_request(3)
    student.add_notification()
    tentative_request.save()
    student.save()
    return render(request, "polls/confirm_update.html", {'status': "Accepted"})


def tutor_complete(request, s_request_id):
    finished_request = TutorRequest.objects.get(id=s_request_id)
    student = finished_request.student
    finished_request.update_request(5)
    student.add_notification()
    finished_request.save()
    student.save()
    return render(request, "polls/confirm_update.html", {'status': "completed"})


def archive_request_student(request, t_request_id):
    student = Student.objects.get(user=request.user)
    tr = TutorRequest.objects.get(id=t_request_id)
    tr.archive()
    tr.save()
    args = format_requests(student)
    return render(request, 'polls/new_student_page.html', args)


def archive_request_tutor(request, s_request_id):
    tutor = Student.objects.get(user=request.user)
    tr = TutorRequest.objects.get(id=s_request_id)
    tr.archive(True)
    tr.save()
    print(tr.tutor)
    args = format_requests(tutor, True)
    return render(request, 'polls/new_tutor_page.html', args)

def redirect_chat_tutor(request, s_request_id):
    tr = TutorRequest.objects.get(id=s_request_id)
    chat_room =  tr.configure_url()
    return HttpResonseRedirect(chat_room)

def redirect_chat_student(request, t_request_id):
    tr = TutorRequest.objects.get(id=t_request_id)
    chat_room = tr.configure_url()
    return HttpResponseRedirect(chat_room)
