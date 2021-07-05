from django.urls import path, include

from api import views

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('registration/', views.RegistrationView.as_view())
]