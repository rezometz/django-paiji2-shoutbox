import django
from django.test import TestCase  # , Client
from htmlvalidator.client import ValidatingClient
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from paiji2_shoutbox.models import (
    Note as Message,
)
# from paiji2_shoutbox.views import (
#     NoteListView as MessageListView,
#     NoteCreateView as MessageCreateView,
#     NoteEditView as MessageEditView,
#     NoteDeleteView as MessageDeleteView,
# )


def reload_object(obj):
    if django.VERSION[0] >= 1 and django.VERSION[1] >= 8:
        obj.refresh_from_db()
        return obj
    else:
        return obj._meta.model.objects.get(pk=obj.pk)


User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            'alice',
            password='test',
        )
        self.chuck = User.objects.create_user(
            'chuck',
            password='test',
        )
        self.message = Message.objects.create(
            author=self.alice,
            message='test',
        )
        self.client = ValidatingClient()


class PagesTestCase(BaseTestCase):
    def test_list(self):
        url = reverse('message-list')

        # Unauthenticated user
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        # Authenticated user
        self.client.login(username='alice', password='test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        url = reverse('message-add')
        # Unauthenticated user
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        # Authenticated user
        self.client.login(username='alice', password='test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {
            'message': 'test',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 2)

    def test_edit(self):
        url = reverse('message-edit', kwargs={
            'pk': self.message.pk,
        })

        # Non owner
        self.client.login(username='chuck', password='test')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

        # Owner
        self.client.login(username='alice', password='test')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {
            'message': 'retest',
            'next': reverse('message-list'),
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 1)
        self.message = reload_object(self.message)
        self.assertEqual(self.message.message, 'retest')

    def test_delete(self):
        url = reverse('message-delete', kwargs={
            'pk': self.message.pk,
        })
        # Non owner
        self.client.login(username='chuck', password='test')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

        # Owner
        self.client.login(username='alice', password='test')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 0)
