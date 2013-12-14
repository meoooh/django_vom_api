# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from rest_framework import routers

from vom import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet)

urlpatterns = patterns('vom',
    url(r'^', include(router.urls)),
    # url(r'^users/?$', views.UserViewSet.as_view(),
    #     name='vomuser-list'),
    # url(r'^users/(?P<pk>\d+)/?$', views.UserViewSet.as_view(),
    #     name='vomuser-detail'),
    # url(r'^users/?$', 'views.createUser', name='createUser'),
    # url(r'^users/(?P<pk>\d+)/change-password/?$', 'views.changePassword',
    #   name='changePassword'),
)
