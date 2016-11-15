from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^question/(?P<question_num>[0-9]+)/$', views.question, name='question'),
    url(r'^answer/(?P<question_num>[0-9]+)/$', views.answer, name='answer'),
]
