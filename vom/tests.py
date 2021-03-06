# -*- coding: utf-8 -*-
import datetime
from unittest import skip # @skip('blahblah')

from rest_framework.test import APITestCase

from faker import Faker

from .models import *

# Create your tests here.

fake = Faker()

def refresh(model_instance):
    cls = type(model_instance)
    return cls.objects.get(pk=model_instance.pk)


class UserVom(APITestCase):

    def setUp(self):
        toi = TypeOfItem.objects.create(kor=u'별자리', _eng='constellations')
        item = Item.objects.create(kor=u'북극성', _eng='book', number_of_elem=3,
                                    form=toi)
        item2 = Item.objects.create(kor=u'게자리', _eng='gae', number_of_elem=4,
                                    form=toi)
        self.user = VomUser.objects.create_user(
            'h@h.com', 'han', '1990-05-05', 1, 'password'
        )
        self.user.item_which_I_am_collecting = item
        self.user.save()
        # self.client.login(username=self.user.email, password='password')
        data = {'username': 'h@h.com', 'password': 'password'}
        self.client.post('/login', data)
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

        self.assertEqual(True, user.check_password(data.get('new_password')))

    def test_change_birthday_success(self):
        data = {'birthday': '1990-08-11'}
        response = self.client.patch('/accounts/me', data)

        self.assertEqual(200, response.status_code)
        user = refresh(self.user)

        self.assertEqual(
            user.birthday,
            datetime.datetime.strptime(
                data.get('birthday'), '%Y-%m-%d'
            ).date()
        )

    def test_delete_account_success(self):
        response = self.client.delete('/accounts/me')

        self.assertEqual(204, response.status_code)

    def test_logout(self):
        response = self.client.delete('/logout')

        self.assertEqual(204, response.status_code)

    @skip("To Do!!!")
    def test_password_reset(self):
        pass

class AnswerVom(APITestCase):

    def setUp(self):
        toi = TypeOfItem.objects.create(kor=u'별자리', _eng='constellations')
        item = Item.objects.create(kor=u'북극성', _eng='book', number_of_elem=3,
                                    form=toi)
        item2 = Item.objects.create(kor=u'게자리', _eng='gae', number_of_elem=4,
                                    form=toi)
        self.user = VomUser.objects.create_user(
            'h@h.com', 'han', '1990-05-05', 1, 'password'
        )
        self.user.item_which_I_am_collecting = item
        self.user.save()
        # self.client.login(username=self.user.email, password='password')
        self.client.force_authenticate(user=self.user)

        category = Category.objects.create(name="FirstCategory")

        question = Question.objects.create(writer=self.user,
                                        contents='FirstQuestion',
                                        category=category)
        for i in xrange(10):
            Question.objects.create(writer=self.user,
                                            contents=fake.sentence(),
                                            category=category)
        Answer.objects.create(writer=self.user,
                            contents='haha',
                            question=question)

    def test_create_answer(self):
        data = {'contents': 'hmmAnswer'}
        response = self.client.post('/questions/1/answers', data)

        self.assertEqual(201, response.status_code)
        self.assertEqual(2, Answer.objects.count())

    def test_read_answer(self):
        response = self.client.get('/questions/1/answers/1')

        self.assertEqual(200, response.status_code)
        self.assertEqual('haha', response.data.get('contents'))

    def test_modify_answer(self):
        sentence = fake.sentence()

        response = self.client.get(
            '/questions/1/answers/1')

        self.assertNotEqual(sentence, response.data.get('contents'))

        data = {'contents': sentence}
        response = self.client.patch('/questions/1/answers/1', data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(sentence, response.data.get('contents'))

    def test_delete_answer(self):
        self.assertEqual(1, Answer.objects.count())

        response = self.client.delete(
            '/questions/1/answers/1')

        self.assertEqual(0, Answer.objects.count())

    @skip("To Do!!!")
    def test_read_other_user_answer(self):
        pass

    @skip("To Do!!!")
    def test_modifiy_other_user_answer(self):
        pass

    @skip("To Do!!!")
    def test_delete_other_user_answer(self):
        pass

    def test_create_answer_related_question_of_today_with_question(self):
        qt = self.client.get('/questions/question-of-today').data

        data = {'contents': fake.sentence()}
        response = self.client.post('/questions/question-of-today/answers', data)

        self.assertEqual(201, response.status_code)
        self.assertTrue(response.has_header('location'))
        self.assertEqual(response.data.get('question'), qt.get('id'))

    def test_create_answer_related_question_of_today_without_question(self):
        data = {'contents': fake.sentence()}
        response = self.client.post('/questions/question-of-today/answers',
                                    data)

        self.assertEqual(201, response.status_code)

        qt = self.client.get('/questions/question-of-today/').data

        self.assertEqual(response.data.get('question'), qt.get('id'))

class QuestionVom(APITestCase):

    def setUp(self):
        toi = TypeOfItem.objects.create(kor=u'별자리', _eng='constellations')
        item = Item.objects.create(kor=u'북극성', _eng='book', number_of_elem=3,
                                    form=toi)
        item2 = Item.objects.create(kor=u'게자리', _eng='gae', number_of_elem=4,
                                    form=toi)
        self.user = VomUser.objects.create_user(
            'h@h.com', 'han', '1990-05-05', 1, 'password'
        )
        self.user.item_which_I_am_collecting = item
        self.user.save()
        # self.client.login(username=self.user.email, password='password')
        self.client.force_authenticate(user=self.user)

        category = Category.objects.create(name=fake.word())
        self.question1 = Question.objects.create(writer=self.user,
                                            contents=fake.sentence(),
                                            category=category)
        self.question2 = Question.objects.create(writer=self.user,
                                                contents=fake.sentence(),
                                                category=category)

        for i in xrange(10):
            Question.objects.create(writer=self.user,
                                    contents=fake.sentence(),
                                    category=category)

        answer1 = Answer.objects.create(writer=self.user,
                                        contents=fake.sentence(),
                                        question=self.question1)

    def test_read_unrecieved_question(self):
        response = self.client.get('/questions/8/')
        self.assertEqual(404, response.status_code)

    def test_get_specific_question(self):
        response = self.client.get('/questions/1/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.data.get('id'))

    def test_get_question_of_today(self):
        """최초에 오늘의 질문을 받았으면, 그날은 몇번을 요청해도 해당 질문을 응답해야한다"""
        response1 = self.client.get('/questions/question-of-today/')
        self.assertEqual(200, response1.status_code)
        self.assertNotEqual(self.question1.pk, response1.data.get('id'))

        response2 = self.client.get('/questions/question-of-today/')
        self.assertEqual(response1.data.get('id'), response2.data.get('id'))

        response3 = self.client.get('/questions/question-of-today/')
        self.assertEqual(response2.data.get('id'), response3.data.get('id'))

class ItemVom(APITestCase):
    def setUp(self):
        toi = TypeOfItem.objects.create(kor=u'별자리', _eng='constellations')
        item = Item.objects.create(kor=u'북극성', _eng='book', number_of_elem=3,
                                    form=toi)
        item2 = Item.objects.create(kor=u'게자리', _eng='gae', number_of_elem=4,
                                    form=toi)
        self.user = VomUser.objects.create_user(
            'h@h.com', 'han', '1990-05-05', 1, 'password'
        )
        self.user.item_which_I_am_collecting = item2
        self.user.save()
        # self.client.login(username=self.user.email, password='password')
        self.client.force_authenticate(user=self.user)

        category = Category.objects.create(name=fake.word())
        self.question1 = Question.objects.create(writer=self.user,
                                            contents=fake.sentence(),
                                            category=category)
        self.question2 = Question.objects.create(writer=self.user,
                                                contents=fake.sentence(),
                                                category=category)

        for i in xrange(10):
            Question.objects.create(writer=self.user,
                                    contents=fake.sentence(),
                                    category=category)

        answer1 = Answer.objects.create(writer=self.user,
                                        contents=fake.sentence(),
                                        question=self.question1)

        Answer.objects.create(writer=self.user,
                            contents=fake.sentence(),
                            question=self.question2)

        item_box = ItemBox.objects.create(owner=self.user)
        item_box.items.add(toi)

        ActivityLog.objects.create(user=self.user, question=self.question1,
                                    item=item)
        ActivityLog.objects.create(user=self.user, question=self.question1,
                                    item=item2)
        ActivityLog.objects.create(user=self.user, question=self.question2,
                                    item=item2)

    def test_get_items(self):
        response = self.client.get('/constellations/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.data.get('count'))

    def test_get_questions_related_item(self):
        response = self.client.get('/constellations/2/questions')

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.data.get('count'))
