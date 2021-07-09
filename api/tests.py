from datetime import datetime
import pytz
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from api.models import MyUser, UserEvent


class RegistrationLoginTest(TestCase):

    def test_registration_login(self):
        url = reverse('api:registration')
        data = {
            "email": "test@mail.ru",
            "password": "3123dsad"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test assert token
        user = MyUser.objects.get(email=data['email'])
        token = Token.objects.get(user_id=user.id)
        self.assertEqual(response.data['token'], token.key)

        # Test login
        url_login = reverse('api:login')
        response = self.client.post(url_login, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], token.key)
        self.assertEqual(response.data['success'], True)

        # Test wrong email
        data_wrong_email = {
            "email": "test_wrong_email",
            "password": "3123dsad"
        }
        response = self.client.post(url, data=data_wrong_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test wrong password
        data_wrong_password = {
            "email": "test@mail.ru",
            "password": "3123dsa"
        }
        response = self.client.post(url_login, data=data_wrong_password)
        self.assertEqual(response.status_code, status.HTTP_418_IM_A_TEAPOT)


class CreateEventTest(TestCase):

    def setUp(self):
        url = reverse('api:registration')
        data = {
            "email": "test@mail.ru",
            "password": "3123dsad"
        }
        response = self.client.post(url, data=data)
        self.user = MyUser.objects.get(email=data['email'])
        self.token = response.data['token']

    def test_create_event(self):
        url = reverse('api:crate_event')
        data = {
            "title": "Test title",
            "start_event": "2021-07-09T12:30",
            "end_event": "2021-07-10T12:30",
            "notification": ""
        }

        # Test without token
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with token
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token,
        }
        response = self.client.post(url, data=data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        event = UserEvent.objects.get(user_id=self.user.id, **response.data)
        self.assertEqual(data['title'], event.title)
        self.assertEqual(data['start_event'], event.start_event.strftime("%Y-%m-%dT%H:%M"))
        self.assertEqual(data['end_event'], event.end_event.strftime("%Y-%m-%dT%H:%M"))
        self.assertEqual(None, event.notification)

        # Test without end_data
        data['title'] = "Test title 2"
        data['end_event'] = ""
        response = self.client.post(url, data=data, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        event = UserEvent.objects.get(user_id=self.user.id, **response.data)
        end_day = datetime.strptime(data['start_event'], "%Y-%m-%dT%H:%M").replace(hour=23, minute=59, tzinfo=pytz.UTC)
        self.assertEqual(end_day, event.end_event)


class ListViewEventsTest(TestCase):

    def setUp(self):
        url = reverse('api:registration')
        data = {
            "email": "test@mail.ru",
            "password": "3123dsad"
        }
        response = self.client.post(url, data=data)
        self.user = MyUser.objects.get(email=data['email'])
        self.token = response.data['token']
        data_1 = {
            "title": "Test title 1",
            "start_event": "2021-07-09T12:30",
            "end_event": "2021-07-10T12:30",
            "notification": ""
        }
        data_2 = {
            "title": "Test title 2",
            "start_event": "2021-07-09T12:30",
            "end_event": "2021-07-10T12:30",
            "notification": ""
        }
        data_3 = {
            "title": "Test title 3",
            "start_event": "2021-07-10T12:30",
            "end_event": "2021-07-10T13:30",
            "notification": ""
        }
        data_4 = {
            "title": "Test title 4",
            "start_event": "2021-08-10T12:30",
            "end_event": "2021-08-10T13:30",
            "notification": ""
        }
        all_data = [data_1, data_2, data_3, data_4]
        url = reverse('api:crate_event')
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token,
        }
        for el_data in all_data:
            self.client.post(url, data=el_data, **auth_headers)

    def test_events_per_day(self):
        url = reverse('api:day_events', kwargs={'year': 2021, 'month': 7, 'day': 9})

        # Test without token
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with token
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token,
        }
        response = self.client.get(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_events_per_month(self):
        url = reverse('api:month_events', kwargs={'year': 2021, 'month': 7})

        # Test without token
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with token
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token,
        }
        response = self.client.get(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)