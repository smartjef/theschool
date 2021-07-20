from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.HomeView.as_view(),name='index'),
    path('register/', views.register, name="register"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('hub',views.hub, name="hub"),
    path('forgot_password', views.forgot_password, name="forgot-password"),
    path('change-password', auth_views.PasswordChangeView.as_view(
        #messages.success(request, "you've successfully changed your password"),
        template_name= 'app_users/change-password.html',
        success_url='/',
        title='password change sucessful'
        ), name="change-password"),
    
    path('profile',views.ProfileView.as_view(), name="profile"),
    path('profile-update',views.ProfileUpdateView.as_view(), name="profile_update"),
    path('settings',views.settings, name="settings"),
    path('contact/', views.ContactView.as_view(), name="contact"),
]