from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question, Suggestion, Student


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


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
    return render(request, 'quick-tutor/chat.html')

def room(request, room_name):
    return render(request, 'quick-tutor/room.html', {
        'room_name': room_name
    })

def index(request):
    context = {
        'questions': Question.objects.order_by('-date')
        if request.user.is_authenticated else []
    }

    return render(request, "polls/index.html", context)



from django.views.generic import ListView


def student_profile(request):
    return render(request, "polls/student_profile.html")

def create_student(request):
    return render(request, "polls/create_student.html")