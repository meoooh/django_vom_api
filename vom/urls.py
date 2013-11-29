# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('vom',
    url(r'^users/?$', 'views.createUser', name='createUser'),
    url(r'^users/(?P<pk>\d+)/change-password/?$', 'views.changePassword',
    	name='changePassword'),
)
