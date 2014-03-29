from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/?$', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/?', include('rest_framework_swagger.urls')),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('vom.urls')),
)
