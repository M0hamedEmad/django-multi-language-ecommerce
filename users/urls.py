from django.urls import path, reverse_lazy
from .views import RegistrationFormView, LoginFormView, logout_view
from django.contrib.auth.views import (PasswordResetView, 
                                    PasswordResetDoneView,
                                    PasswordResetConfirmView,
                                    PasswordResetCompleteView)

app_name = 'users'


urlpatterns = [
    path('register/', RegistrationFormView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        success_url = reverse_lazy("users:password_reset_done"),
        ), name='password_reset'),
    
    path('password_reset_done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
        ), name='password_reset_done'),
    
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url = reverse_lazy("users:password_reset_complete"),
        ), name='password_reset_confirm'),
    
        path('password_reset_complete/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html',
        ), name='password_reset_complete'),
]