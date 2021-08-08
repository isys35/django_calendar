from django.contrib.auth import authenticate, login
from datetime import datetime

from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.tasks import notification
from api.models import MyUser, UserEvent, CountryHoliday
from api.serializers import RegistrationUserSerializer, LoginUserSerializer, CreateEventUserSerializer, \
    HolidaysSerializer, UpdaterSerializer


class RegistrationView(APIView):
    serializer_class = RegistrationUserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'country' in request.data:
            user = MyUser(email=request.data['email'], country_id=request.data['country'])
        else:
            user = MyUser(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    serializer_class = LoginUserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=serializer.data['email'], password=serializer.data['password'])
        if user is not None:
            login(request, user)
            token = Token.objects.get(user_id=user.id)
            return Response({"success": True, "token": token.key}, status=status.HTTP_200_OK)
        return Response({"success": False}, status=status.HTTP_418_IM_A_TEAPOT)


class CreateEventView(APIView):
    serializer_class = CreateEventUserSerializer

    # Todo: delete auth
    # authentication_classes = [BasicAuthentication, SessionAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = UserEvent(**serializer.data)
        event.user = request.user
        event.save()
        if event.notification:
            notification.apply_async((event.user.email, event.title, event.start_event, event.end_event),
                                     eta=datetime.utcnow() - event.notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventsDayView(ListAPIView):
    queryset = UserEvent.objects
    serializer_class = CreateEventUserSerializer

    def list(self, request, year, month, day, **kwargs):
        queryset = self.queryset.filter(start_event__day=day,
                                        start_event__month=month,
                                        start_event__year=year)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventsMonthView(EventsDayView):

    def list(self, request, year, month, **kwargs):
        queryset = self.queryset.filter(start_event__month=month,
                                        start_event__year=year)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HolidaysMonthView(ListAPIView):
    queryset = CountryHoliday.objects
    serializer_class = HolidaysSerializer

    def list(self, request, year, month):
        queryset = self.queryset.filter(date__month=month,
                                        date__year=year, country_id=request.user.country_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IntervalUpdate(APIView):
    serializer_class = UpdaterSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        PeriodicTask.objects.create(
            name='Update countries and holidays',
            task='update_countries_holidays',
            interval=IntervalSchedule.objects.get_or_create(every=serializer.data['every'],
                                                            period=serializer.data['period'])[0],
            start_time=datetime.now(),
        )
        return Response({"status": True}, status=status.HTTP_201_CREATED)
