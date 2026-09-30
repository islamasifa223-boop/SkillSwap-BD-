from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.login_view, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('logout/', views.logout_view, name='logout'),

    path('create-profile/', views.create_profile, name='create_profile'),

    path('add-skill/', views.add_skill, name='add_skill'),

    path('skills/', views.skill_list, name='skill_list'),

    path( 'send-request/<int:skill_id>/', views.send_request,
    name='send_request'),

    path('requests/', views.request_list, name='request_list'),

    path('accept-request/<int:request_id>/', views.accept_request,name='accept_request'),

    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),

    path('like/<int:skill_id>/', views.like_skill, name='like_skill'),

    path('like/<int:skill_id>/', views.like_skill, name='like_skill'),

    path('notifications/', views.notifications, name='notifications'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),

    path('chat/<int:user_id>/', views.chat, name='chat'),

    path('edit-skill/<int:skill_id>/', views.edit_skill, name='edit_skill'),

    path('delete-skill/<int:skill_id>/', views.delete_skill, name='delete_skill'),

    path('create-session/<int:request_id>/', views.create_session, name='create_session'),

    path('sessions/', views.session_list, name='session_list'),

    path('add-review/<int:session_id>/', views.add_review, name='add_review'),
    
    path('recommendations/', views.recommendations, name='recommendations'),

    path('ai-match/', views.ai_match, name='ai_match'),


]