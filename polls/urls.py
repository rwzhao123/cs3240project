from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import include, path
from django.conf import settings

app_name = 'quick-tutor'
urlpatterns = [
    url(r'$^', views.index),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('suggestions/', views.suggestions, name='suggestions'),
    path('suggestions/list/', views.suggestions_list, name='suggestions_lists'),
    path('', include('social_django.urls', namespace='social')),
    path(r'^logout/$', LogoutView, {'next_page': settings.LOGOUT_REDIRECT_URL},
         name='logout'),

    path('student_profile/', views.update_profile),
    path('edit_student_profile/', views.edit_info, name = 'edit_info'),
    path(r'^profile/$',views.update_profile),
    path('student_profile/requests/', views.student_requests),
    path('student_profile/requests/new_request', views.create_request),

    path('chat/', views.chat, name='chat'),
    path('chat/<str:room_name>/', views.room, name='room'),


    path('register_as_student/', views.create_student),

    url(r'^tutor_matches/(?P<student>[a-zA-Z0-9]+)/$', views.add_student, name='add_student'),

    path('about/', views.about),
    path('tutor_match/', views.AllStudentsView.as_view(), name='match'),
    path('tutor_match/confirm', views.confirm_match),
    path('tutor_page/', views.show_requests, name = 'show_requests'),

    path('contact_us/', views.contact_us),

]