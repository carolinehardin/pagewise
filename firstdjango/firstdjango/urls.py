from django.conf.urls import include, url
from django.contrib import admin

from inventory import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^item/(?P<id>\d+)/', views.item_detail, name='item_detail'),
    url(r'^studySession/(?P<id>\d+)/', views.studySession_detail, name='studySession_detail'),
    url(r'^course/(?P<id>\d+)/', views.course_detail, name='course_detail'),
    url(r'^admin/', include(admin.site.urls)),
]
