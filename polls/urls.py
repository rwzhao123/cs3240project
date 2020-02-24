from django.urls import path

from . import views
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import include, path
from django.conf import settings

app_name = 'quick-tutor'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('suggestions/', views.suggestions, name='suggestions'),
    path('suggestions/list/', views.suggestions_list, name='suggestions_lists'),
    path('', include('social_django.urls', namespace='social')),
    path(r'^logout/$', LogoutView, {'next_page': settings.LOGOUT_REDIRECT_URL},
         name='logout'),

    path('chat/', views.chat, name='chat'),
    path('chat/<str:room_name>/', views.room, name='room')

    path('student_profile/', views.student_profile),
    path('register_as_student/', views.create_student),

]