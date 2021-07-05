from django.urls import path, include

from api import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('registration/', views.RegistrationView.as_view()),
    path('create-event/', views.CreateEventView.as_view()),
]
