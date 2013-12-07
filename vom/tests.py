import datetime
from unittest import skip

from rest_framework.test import APITestCase

from .models import *

# Create your tests here.


class Vom(APITestCase):

    def setUp(self):
        VomUser.objects.create_user(
            'h@h.com', 'han', '1990-05-05', 1, 'password'
        )

    def test_create_user_multipart_success(self):
        data = {'email': 'ha@h.com', 'sex': 1, 'name': 'ha', 'password': '1313',
                'password2': '1313', 'birthday': '1990-06-06'}
        response = self.client.post('/users', data)

        self.assertEqual(response.status_code, 201)

    def test_create_user_json_success(self):
        data = {'email': 'ha@h.com', 'sex': 1, 'name': 'ha', 'password': '1313',
                'password2': '1313', 'birthday': '1990-06-06'}
        response = self.client.post('/users', data, format='json')

        self.assertEqual(response.status_code, 201)

    def test_create_user_birthday_is_not_exist(self):
        response = self.client.post('/users')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 6)

    def test_change_password_success(self):
        data = {'old_password': '1313', 'new_password': '1212',
                'new_password2': '1212'}
        response = self.client.post('/users/1/change-password', data)

        self.assertEqual(response.status_code, 204)
