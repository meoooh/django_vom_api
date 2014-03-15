# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from vom import views

router = routers.SimpleRouter(trailing_slash=False)
# router.register(r'users', views.UserViewSet)
# router.register(r'answers', views.AnswerViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'categories', views.CategoryViewSet)
# router.register(r'constellations', views.ConstellationViewSet)
# router.register(r'items', views.ItemViewSet)

# questions_router = NestedSimpleRouter(router, r'users', lookup='user',
#                                     trailing_slash=False)
# questions_router.register(r'questions', views.QuestionViewSet, 
#                             base_name='question',)

answers_router = NestedSimpleRouter(router, r'questions',
                                    lookup='question',
                                    trailing_slash=False)
# router.register(r'answers', views.AnswerCreationSet)
# router.register(r'answers/(?<pk>\d+)/?$', views.AnswerDetailViewSet)

urlpatterns = patterns('vom',
    url(r'^accounts/?$', views.UserCreationSet.as_view()),
    url(r'^accounts/me/?$', views.UserDetailViewSet.as_view(), name='accounts'),

    url(r'^questions/(?P<question_pk>\d+)/answers/?$',
        views.AnswerCreationSet.as_view()),
    url(r'^questions/(?P<question_pk>\d+)/answers/(?P<pk>\d+)/?$',
        views.AnswerDetailViewSet.as_view(), name='answer-detail'),

    url(r'^', include(router.urls)),
    # url(r'^', include(questions_router.urls)),
    url(r'^', include(answers_router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls',namespace='rest_framework')),
    # url(r'^users/?$', views.UserViewSet.as_view(),
    #     name='vomuser-list'),
    # url(r'^users/(?P<pk>\d+)/?$', views.UserViewSet.as_view(),
    #     name='vomuser-detail'),
    # url(r'^users/?$', 'views.createUser', name='createUser'),
    url(r'^accounts/me/settings/change-password/?$', 'views.changePassword',
      name='changePassword'),
)
