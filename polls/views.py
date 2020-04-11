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

def chat(request):
    return render(request, 'polls/chat.html')

def room(request, room_name):
    return render(request, 'polls/room.html', {
        'room_name': room_name
    })

def index(request):
    print("this was called")
    return render(request, "polls/index.html")



from django.views.generic import ListView

class StudentView(ListView):
    template_name = ""

def student_profile(request):
    return render(request, "polls/edit_student_profile.html")

#def my_requests(request):

@login_required
def update_profile(request):
    print("this was called")
    #if request.method == 'POST':
        #print("yay")
        #user_form = UserForm(request.POST,instance=request.user)
        #profile_form = ProfileForm(request.POST, instance = request.user.profile)
        #choice_form = ChoiceForm(request.POST)
        #if profile_form.is_valid():
        #if user_form.is_valid() and profile_form.is_valid() and choice_form.is_valid():
            #print("here")
            ##user_form.save()
            #post = profile_form.save(commit=False)
            #post.user = request.user
            
            #post.save()

            #instance = choice_form.save(commit=False)
            #instance.user = request.user
            #choice_form.save()
            #return render(request,"polls/student_profile.html", {"profile_form": profile_form})
            #return render(request,"polls/edit_student_profile.html",{"user_form": user_form, "profile_form": profile_form, "choice_form": choice_form})
    #else:
        #print("no here")
        #user_form = UserForm(instance = request.user)
        #profile_form = ProfileForm(instance = request.user.profile)
        #choice_form=ChoiceForm(instance=request.user)
    return render(request,"polls/student_profile.html")

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
        return render(request,"polls/edit_student_profile.html", {"profile_form" : profile_form})
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

def add_student(request, student_id):
    requested_user = User.objects.get(id=student_id)
    #requested_user=User.objects.get(id=student_id) 
    requested_student = requested_user.profile
    requested_student.requested.add(request.user)
    print("hello")
    print(requested_student.requested.all())
    return redirect('quick-tutor:confirm')
    

@login_required
def show_requests(request):
    if request.method == "POST":
        print("TUTOR PAGE")
        tutor_form = TutorForm(request.POST, instance=request.user.profile)
        if tutor_form.is_valid():
            tutor_form.save()
            return HttpResponseRedirect("/quick-tutor/tutor_match") # later change this to be a page that says like tutor is on their way
    else:
        print("hm what is this")
        tutor_form = TutorForm(instance=request.user.profile)
        print(tutor_form)
        return render(request, "polls/tutor_page.html", {"tutor_form": tutor_form})

def student_requests(request):
    r = TutorRequest.objects.all(filter=request.Student)
    args = {'sr' : r}
    return render(request, "polls/student_requests.html", args)


def create_request(request):
    TutorRequest.objects.create(student = request.Student, pub_date = timezone.now())
    return render(request, "polls/request.html")

def send_request(request):
    if request.method == "POST":
        request_form = RequestForm(request.POST, instance=request.TutorRequest)
        if request_form.is_valid():
            request_form.save()
    else:
        request_form = RequestForm(instance=request.TutorRequest)
        args = {'request_form': request_form}
        return render(request, "polls/request.html")



class AllStudentsView(generic.ListView):
    student_list = Student.objects.all()
    template_name = 'polls/tutor_match.html'
    def get_queryset(self):
        return Student.objects.all()
