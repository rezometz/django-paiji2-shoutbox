from django.conf.urls import url  # , patterns

from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    url(
        r'^$',
        login_required(views.NoteListView.as_view()),
        name="message-list",
    ),
    url(
        r'^add$',
        login_required(views.NoteCreateView.as_view()),
        name="message-add",
    ),
    url(
        r'^edit/(?P<pk>[0-9]+)/$',
        login_required(views.NoteEditView.as_view()),
        name="message-edit",
    ),
    url(
        r'^delete/(?P<pk>[0-9]+)/$',
        login_required(views.NoteDeleteView.as_view()),
        name="message-delete",
    ),
]
