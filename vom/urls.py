# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from rest_framework import routers

from vom import views

router = routers.SimpleRouter(trailing_slash=True)
router.register(r'questions', views.QuestionViewSet)
# router.register(r'categories', views.CategoryViewSet)
router.register(r'(?P<item_name>[^/]+)', views.ItemViewSet)

urlpatterns = patterns('vom',
    url(r'^questions/question-of-today/?$', views.question_of_today),
    url(r'^questions/question-of-today/answers/?$',
        views.answer_question_of_today),
    url(r'^accounts/?$', views.UserCreationSet.as_view()),
    url(r'^accounts/me/?$', views.UserDetailViewSet.as_view(), name='accounts'),
    url(r'^questions/(?P<question_pk>\d+)/answers/?$',
        views.AnswerCreationSet.as_view()),
    url(r'^questions/(?P<question_pk>\d+)/answers/(?P<pk>\d+)/?$',
        views.AnswerDetailViewSet.as_view(), name='answer-detail'),
    url(r'^', include(router.urls)),
    url(r'^accounts/me/settings/change-password/?$', views.changePassword,
      name='changePassword'),
    url(r'^(?P<item_name>[^/]+)/(?P<item_pk>\d+)/questions/?$',
        views.QuestionRelatedItemViewSet.as_view()),
    url(r'^logout/?$', views.logout),
)
