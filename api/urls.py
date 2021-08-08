from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from api import views
app_name = 'api'

schema_view = get_schema_view(
   openapi.Info(
      title="Календарь API",
      default_version='v1',
      description="Календарь",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="isysbas@gmail.com"),
      license=openapi.License(name="Without license"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('create-event/', views.CreateEventView.as_view(), name='crate_event'),
    path('events/<int:year>/<int:month>/<int:day>/', views.EventsDayView.as_view(), name='day_events'),
    path('events/<int:year>/<int:month>/', views.EventsMonthView.as_view(), name='month_events'),
    path('holidays/<int:year>/<int:month>/', views.HolidaysMonthView.as_view(), name='month_holidays'),
    path('create_updater/', views.IntervalUpdate.as_view(), name='interval_update'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
]
