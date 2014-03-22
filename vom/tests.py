import datetime
from unittest import skip

from rest_framework.test import APITestCase

from .models import *

# Create your tests here.

def refresh(model_instance):
    cls = type(model_instance)
    return cls.objects.get(pk=model_instance.pk)


class UserVom(APITestCase):

    def setUp(self):
        self.user = VomUser.objects.create_user(
            'h@h.com', 'han', '1990-05-05', 1, 'password'
        )
        # self.client.login(username=self.user.email, password='password')
        self.client.force_authenticate(user=self.user)

    def test_login_success(self):
        data = {'username': 'h@h.com', 'password':'password'}
        response = self.client.post('/login', data)

        self.assertIn('token', response.data)

    def test_create_user_multipart_success(self):
        data = {'email': 'ha@h.com', 'sex': 1, 'name': 'ha', 'password': '1313',
                'password2': '1313', 'birthday': '1990-06-06'}
        response = self.client.post('/accounts', data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(VomUser.objects.count(), 2)

    def test_create_user_json_success(self):
        data = {'email': 'ha@h.com', 'sex': 1, 'name': 'ha', 'password': '1313',
                'password2': '1313', 'birthday': '1990-06-06'}
        response = self.client.post('/accounts', data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(VomUser.objects.count(), 2)

    def test_create_user_birthday_is_not_exist(self):
        response = self.client.post('/accounts')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 6)
        self.assertEqual(VomUser.objects.count(), 1)

    def test_change_password_success(self):
        data = {'current_password': 'password', 'new_password': '1212',
                'new_password2': '1212'}
        response = self.client.patch('/accounts/me/settings/change-password',
                                    data)
        self.assertEqual(response.status_code, 204)

        user = refresh(self.user)

        self.assertEqual(True, user.check_password(data['new_password']))

    def test_change_birthday_success(self):
        data = {'birthday': '1990-08-11'}
        response = self.client.patch('/accounts/me', data)

        self.assertEqual(200, response.status_code)
        user = refresh(self.user)

        self.assertEqual(
            user.birthday,
            datetime.datetime.strptime(
                data['birthday'], '%Y-%m-%d'
            ).date()
        )

    def test_delete_account_success(self):
        response = self.client.delete('/accounts/me')

        self.assertEqual(204, response.status_code)

class AnswerVom(APITestCase):

    def setUp(self):
        self.user = VomUser.objects.create_user(
            'h@h.com', 'han', '1990-05-05', 1, 'password'
        )
        # self.client.login(username=self.user.email, password='password')
        self.client.force_authenticate(user=self.user)

        category = Category.objects.create(name="FirstCategory")

        question = Question.objects.create(writer=self.user, 
                                        contents='FirstQuestion',
                                        category=category)
        Answer.objects.create(writer=self.user,
                            contents='haha',
                            question=question)

    def test_create_answer(self):
        data = {'contents': 'hmmAnswer'}
        response = self.client.post('/questions/1/answers', data)

        self.assertEqual(201, response.status_code)
        self.assertEqual(2, Answer.objects.count())
