from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Suggestion, Student, TutorRequest
from .forms import RequestForm

#from .forms import UserForm, ProfileForm, ChoiceForm
from .forms import ProfileForm, TutorForm




class IndexView(generic.ListView):
    template_name = 'polls/index.html'


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def suggestions(request):
    return render(request, "polls/suggestions.html")

def suggestions_list(request):

    list_of_suggestions = Suggestion.objects.all()
    entry = request.POST.get("suggestion_text")
    q = Suggestion(suggestion_text = entry)
    q.save()
    context = {

        "suggestion_text" : list_of_suggestions
    }
    return render(request, "polls/list.html", context)


def index(request):
    return render(request, "polls/new_index.html")


def chat(request):
    return render(request, 'polls/chat.html')

def room(request, room_name):
    return render(request, 'polls/room.html', {
        'room_name': room_name
    })

from django.views.generic import ListView

class StudentView(ListView):
    template_name = ""

def student_profile(request):
    return render(request, "polls/new_edit_profile.html")

#def my_requests(request):

@login_required
def update_profile(request):
    print("this was called")
    return render(request,"polls/new_profile.html")

        #return render(request,"polls/edit_student_profile.html",{"user_form": user_form, "profile_form": profile_form, "choice_form": choice_form})
@login_required
def edit_info(request):
    if request.method ==  "POST":
        print("in here")
        profile_form = ProfileForm(request.POST, instance= request.user.profile)
        #request_form = RequestForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
        #if profile_form.is_valid() and request_form.is_valid():
            profile_form.save()
            #request_form.save()
            return HttpResponseRedirect("/quick-tutor/student_profile")
            #return render(request, "polls/student_profile.html")
    else:
        print("this happend")

        profile_form = ProfileForm(instance=request.user.profile)
        #request_form = RequestForm(instance=request.user.profile)
        print(profile_form)
        return render(request,"polls/new_edit_profile.html", {"profile_form" : profile_form})
        #return render(request,"polls/edit_student_profile.html", {"profile_form" : profile_form, "request_form": request_form})

def create_student(request):
    return render(request, "polls/create_student.html")

def about(request):
    return render(request, "polls/about.html")

def tutor_match(request):
    return render(request, "polls/tutor_match.html")

def contact_us(request):
    return render(request, "polls/contact_us.html")

def confirm_match(request):
    return render(request, "polls/confirm_match.html")

def error_match(request):
    return render(request, "polls/error_match.html")

def add_student(request, student_id):


    requested_user = User.objects.get(id=student_id)
    #requested_user=User.objects.get(id=student_id) 
    requested_student = requested_user.profile
    requested_student.requested.add(request.user)
    request.user.profile.my_requests.add(requested_user)
    return redirect('quick-tutor:confirm')

def cancel_tutor(request, tutor_id):
    canceled_user = User.objects.get(id=tutor_id)
    canceled_tutor = canceled_user.profile
    print(canceled_tutor.requested)
    canceled_tutor.requested.remove(request.user)
    request.user.profile.my_requests.remove(canceled_user)
    return redirect('quick-tutor:confirm_cancel')


def confirm_cancel(request):
    return render(request, "polls/confirm_cancel.html")

def deny_request(request, student_id):
    
    return render(request, "polls/tutor_page.html")


@login_required
def show_requests(request):
    # if request.method == "POST":
    #     print("TUTOR PAGE")
    #     tutor_form = TutorForm(request.POST, instance=request.user.profile)
    #     if tutor_form.is_valid():
    #         tutor_form.save()
    #         return HttpResponseRedirect("/quick-tutor/tutor_match")
    # else:
    #     print("hm what is this")
    #     tutor_form = TutorForm(instance=request.user.profile)
    #     print(tutor_form)
    #     return render(request, "polls/tutor_page.html", {"tutor_form": tutor_form})
    return render (request, "polls/tutor_page.html")

def student_requests(request):

    s = Student.objects.get(user = request.user)
    print(s)
    r = TutorRequest.objects.filter(student = s)
    print(r)
    for obj in r:
        if obj.is_old() and (obj.progress == 'Declined'or obj.progress == 'Canceled'):
            TutorRequest.objects.filter(id=obj.id).delete()
    print("Requests found",r)
    if len(r) <=0:
        r = 0
    args = {'sr' : r }
    return render(request, "polls/student_requests.html", args)

def tutor_requests(request):
    canceled = 0
    declined = 0
    pending = 0
    accepted = 0
    t = Student.objects.get(user=request.user)
    r = TutorRequest.objects.filter(tutor = t)
    r_num = len(r)
    for obj in r:
        if obj.progress == 'Denied' or obj.progress == 'Canceled':
            if obj.is_old():
                TutorRequest.objects.filter(id=obj.id).delete()
            elif obj.progress == 'Denied':
                declined +=1
            else:
                canceled += 1
        elif obj.progress == 'Pending':
            pending += 1
        elif obj.progress == 'Accepted':
            accepted += 1
    print("Requests found", r)
    if len(r) <= 0:
        r = 0
    args = {'tr': r, 'tr_num': r_num, 'tr_c': canceled, 'tr_d': declined, 'tr_a': accepted, 'tr_p': pending}
    return render(request, "polls/tutor_requests.html", args)




def create_request(request, student_id):

    requested_user = User.objects.get(id=student_id)
    tutor_requested = Student.objects.get(user=requested_user)
    student_requester = Student.objects.get(user=request.user)
    tr = TutorRequest.objects.create(student=student_requester, tutor=tutor_requested, pub_date=timezone.now())
    tr.subject = request.POST['tutor_subject']
    tr.subject_text = request.POST['tutor_additional']
    tr.contact_info = request.POST['contact_method']
    tr.save()
    return redirect('quick-tutor:confirm')

def send_request(request):
    if request.method == "POST":
        request_form = RequestForm(request.POST, instance=request.TutorRequest)
        if request_form.is_valid():
            request_form.save()
    else:
        request_form = RequestForm(instance=request.TutorRequest)
        args = {'request_form': request_form}
        return render(request, "polls/request.html")

def student_page(request):
    return render(request, "polls/student_page.html")


class AllStudentsView(generic.ListView):
    student_list = Student.objects.all()
    template_name = 'polls/tutor_match.html'
    def get_queryset(self):
        return Student.objects.all()

def additional_info(request):
    tutor_id = request.POST['tutor']
    tutor = Student.objects.get(id=tutor_id)
    return render(request, 'polls/additional_info.html', {'tutor':tutor, 'tutor_id': tutor_id})

def student_cancel(request, t_request_id):
    canceled_request = TutorRequest.objects.get(id=t_request_id)
    canceled_request.update_request('Canceled')
    canceled_request.save()
    return redirect("quick-tutor:confirm_cancel")

def tutor_update_request(request, s_request_id):
    tentative_request = TutorRequest.objects.get(id=s_request_id)
    status = request.POST['request_status']
    tentative_request.update_request(status)
    tentative_request.save()
    return render(request,'polls/confirm_update_request.html',{'status':status})

