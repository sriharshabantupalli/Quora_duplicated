from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('add_question/', views.add_question, name='add_question'),
    path('answer_question/<int:question_id>/', views.answer_question, name='answer_question'),
    path('add_comment/<int:question_id>/', views.add_comment, name='add_comment_to_question'),
    path('add_comment/<int:answer_id>/', views.add_comment, name='add_comment_to_answer'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]