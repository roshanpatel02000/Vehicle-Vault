from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/',         views.userSignupView,      name='signup'),
    path('login/',          views.userLoginView,        name='login'),
    path('logout/',         views.userLogoutView,       name='logout'),
    path('verify-otp/',     views.verifyOtpView,        name='verify_otp'),
    path('resend-otp/',     views.resendOtpView,        name='resend_otp'),
    path('forgot-password/',views.forgotPasswordView,   name='forgot_password'),
    path('reset-password/', views.resetPasswordView,    name='reset_password'),
    path('profile/settings/',views.profileSettingsView, name='profile_settings'),
]