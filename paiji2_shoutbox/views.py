from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound
from django.utils.translation import ugettext as _
# from django.conf import settings
# from django.contrib import messages

from paiji2_utils.views import SuccessUrlMixin

from .models import Note
from .forms import NoteForm


class MySuccessUrl(SuccessUrlMixin):

    default_url_name = 'message-list'

    def get_forbidden_urls(self):
        if hasattr(self, 'object'):
            return (
                reverse('message-edit', args=[self.object.pk]),
                reverse('message-delete', args=[self.object.pk]),
            )
        else:
            return None


class OwnershipCheck(object):
    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update notes """
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponseNotFound(
                _('Rezo is not hacked. You don\'t have the permission xD')
            )
        return super(OwnershipCheck, self).dispatch(request, *args, **kwargs)


class NoteListView(generic.ListView):
    model = Note
    paginate_by = 25
    context_object_name = 'notes'
    template_name = 'shoutbox/message/list.html'

    def get_context_data(self, **kwargs):
        context = super(NoteListView, self).get_context_data(**kwargs)
        context.update({
            'form': NoteForm(),
        })
        return context

    def get_queryset(self):
        return super(NoteListView, self).get_queryset().select_related(
            'author'
        )


class NoteCreateView(MySuccessUrl, generic.CreateView):
    model = Note
    fields = ('message', )
    message_success = _(
        """Your note has been added to the board, """
        """it will be displayed in a moment"""
    )
    template_name = 'shoutbox/message/form.html'
    forbidden_url_names = (
        'message-add',
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NoteCreateView, self).form_valid(form)


class NoteEditView(OwnershipCheck, MySuccessUrl, generic.UpdateView):
    model = Note
    fields = ('message', )
    template_name = 'shoutbox/message/form.html'
    message_success = _(
        'Your note has been updated, it will be refreshed in a moment'
    )


class NoteDeleteView(OwnershipCheck, MySuccessUrl, generic.DeleteView):
    model = Note
    template_name = 'shoutbox/note_confirm_delete.html'
    message_success = _(
        'Your note has been removed, it will be refreshed in a moment'
    )
