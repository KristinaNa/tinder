# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.conf.urls import url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import TemplateView

from mytinder import settings
from . import views

urlpatterns = [
    url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^login/$', views.LoginFormView.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),

    #url(r'^$', TemplateView.as_view(template_name='history.html'), name='main'),
    url(r'^$', views.History.as_view()),

    url(r'^my_photos/$', views.List.as_view()),
    url(r'^photos/$', views.Photos.as_view()),

]
