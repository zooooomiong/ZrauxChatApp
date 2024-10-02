from django.urls import path
from  . import views

urlpatterns = [
      path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name="signup"),
      path('confirm-email/', views.confirm_email, name='confirm_email'),
    path('email-confirmed/', views.email_confirmed_view, name='email_confirmed'),
    path("logout/", views.logout_view, name="logout"),
]
