from django.urls import path, include

from api import views
app_name = 'api'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('create-event/', views.CreateEventView.as_view(), name='crate_event'),
    path('events/<int:year>/<int:month>/<int:day>/', views.EventsDayView.as_view(), name='day_events'),
    path('events/<int:year>/<int:month>/', views.EventsMonthView.as_view(), name='month_events'),
    path('holidays/<int:year>/<int:month>/', views.HolidaysMonthView.as_view(), name='month_holidays'),
]
