from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.views.generic.base import RedirectView
app_name = 'quick-tutor'
urlpatterns = [
    url(r'$^', views.index),
    path('', include('social_django.urls', namespace='social')),
    path(r'^logout/$', LogoutView, {'next_page': settings.LOGOUT_REDIRECT_URL},
         name='logout'),
    path('tutor_match/new_additional_info/<int:student_id>', views.additional_info, name='additional_info'),
    path('student_profile/', views.update_profile, name = 'student_profile'),
    path('student_profile/edit/', views.edit_info, name = 'edit'),
    path(r'^profile/$',views.update_profile),
    path('student_profile/requests/', views.student_requests),
    path('student_profile/requests/new_request', views.create_request),

    #path('chat/', views.chat, name='chat'),
    path('chat/<str:room_name>/', views.room, name='room'),

    #path('register_as_student/', views.create_student),

   # path('tutor_match/<int:student_id>/', views.add_student, name='add_student'),
    path('tutor_match/<int:student_id>/', views.create_request, name ='create_request'),
    path('about/', views.about),
    path('tutor_match/', views.AllStudentsView.as_view(), name='tutor_match'),
    path('tutor_match/confirm/', views.confirm_match, name='confirm'),
    path('tutor_match/error/', views.error_match, name='error_match'),
    path('student_requests/', views.student_requests, name = 'student_requests'),
    path('student_requests/<int:t_request_id>/', views.student_cancel, name = 'student_cancel'),
    path('tutor_requests/', views.tutor_requests, name = 'tutor_requests'),
    path('contact_us/', views.contact_us),
    path('become-available/', views.become_available, name = 'become_available'),
    path('tutor-accept/<int:s_request_id>', views.tutor_accept, name = 'tutor_accept'),
    path('tutor-decline/<int:s_request_id>', views.tutor_decline, name = 'tutor_decline'),
    path('tutor-complete/<int:s_request_id>', views.tutor_complete, name = 'tutor_complete'),
    path('confirm_cancel/', views.confirm_cancel, name = 'confirm_cancel'),
    path('student-archive/<int:t_request_id>', views.archive_request_student, name = 'archive_request_student'),
    path('tutor-archive/<int:s_request_id>', views.archive_request_tutor, name = 'archive_request_tutor'),
    path('chat/<int:t_request_id>', views.redirect_chat_student, name='redirect_chat_student'),
    path('chat/<int:s_request_id>', views.redirect_chat_tutor, name='redirect_chat_tutor')

]