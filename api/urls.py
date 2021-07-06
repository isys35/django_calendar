from django.urls import path, include

from api import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('registration/', views.RegistrationView.as_view()),
    path('create-event/', views.CreateEventView.as_view()),
    path('events/<int:year>/<int:month>/<int:day>/', views.EventsDayView.as_view()),
    path('events/<int:year>/<int:month>/', views.EventsMonthView.as_view()),
]
