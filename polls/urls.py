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

    path('student_profile/', views.update_profile, name = 'student_profile'),
    path('student_profile/edit/', views.edit_info, name = 'edit'),
    path(r'^profile/$',views.update_profile),
    path('student_profile/requests/', views.student_requests),
    path('student_profile/requests/new_request', views.create_request),

    #path('chat/', views.chat, name='chat'),
    path('chat/<str:room_name>/', views.room, name='room'),

    #path('register_as_student/', views.create_student),

    path('tutor_match/<int:student_id>/', views.add_student, name='add_student'),
    path('tutor_match/<int:student_id>/', views.create_request, name ='create_request'),
    path('about/', views.about),
    path('tutor_match/', views.AllStudentsView.as_view(), name='match'),
    path('tutor_match/confirm/', views.confirm_match, name='confirm'),
    path('tutor_match/error/', views.error_match, name='error_match'),
    path('tutor_page/', views.show_requests, name = 'show_requests'),
    path('student_page/', views.student_page, name = 'student_page'),
    path('student_page/<int:tutor_id>/', views.cancel_tutor, name = 'cancel_tutor'),
    path('student_page/confirm_cancel/', views.confirm_cancel, name = 'confirm_cancel'),
    path('student_requests/', views.student_requests, name = 'student_requests'),
    path('student_requests/<int:t_request_id>/', views.cancel_ontutor, name = 'cancel_ontutor'),
    path('tutor_requests/', views.tutor_requests, name = 'tutor_requests'),
    path('tutor_requests/<int:s_request_id>/', views.cancel_onstudent, name = 'cancel_onstudent'),
    path('contact_us/', views.contact_us),

]