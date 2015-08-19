from django.conf.urls import patterns, url

from django.contrib.auth.decorators import login_required

from .views import *


urlpatterns = [
    url(
        r'^$',
        login_required(NoteListView.as_view()),
        name="message-list",
    ),
    url(
        r'^add$',
        login_required(NoteCreateView.as_view()),
        name="message-add",
    ),
    url(
        r'^edit/(?P<pk>[0-9]+)/$',
        login_required(NoteEditView.as_view()),
        name="message-edit",
    ),
    url(
        r'^delete/(?P<pk>[0-9]+)/$',
        login_required(NoteDeleteView.as_view()),
        name="message-delete",
    ),
]
