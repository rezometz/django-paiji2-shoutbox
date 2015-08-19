from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from paiji2_shoutbox.models import (
    Note as Message,
)
from paiji2_shoutbox.views import (
    NoteListView as MessageListView,
    NoteCreateView as MessageCreateView,
    NoteEditView as MessageEditView,
    NoteDeleteView as MessageDeleteView,
)
from paiji2_shoutbox.templatetags.shoutbox import (
    display_bulletin_board as display_shoutbox,
    urlize2,
)


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
        self.client = Client(enforce_csrf_checkts=True)


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

