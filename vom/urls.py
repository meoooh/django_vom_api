# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from rest_framework import routers

from vom import views

router = routers.SimpleRouter(trailing_slash=True)
router.register(r'questions', views.QuestionViewSet)
# router.register(r'categories', views.CategoryViewSet)
router.register(r'constellations', views.ConstellationViewSet)

urlpatterns = patterns('vom',
    url(r'^questions/question-of-today/?$', views.questionOfToday),
    url(r'^accounts/?$', views.UserCreationSet.as_view()),
    url(r'^accounts/me/?$', views.UserDetailViewSet.as_view(), name='accounts'),
    url(r'^questions/(?P<question_pk>\d+)/answers/?$',
        views.AnswerCreationSet.as_view()),
    url(r'^questions/(?P<question_pk>\d+)/answers/(?P<pk>\d+)/?$',
        views.AnswerDetailViewSet.as_view(), name='answer-detail'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/me/settings/change-password/?$', views.changePassword,
      name='changePassword'),
)
