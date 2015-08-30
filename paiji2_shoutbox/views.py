from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib import messages

from .models import Note
from .forms import NoteForm


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


class MessageRedirect(object):
    message_success = None

    def get_success_url(self):
        if self.message_success is not None:
            messages.success(
                self.request,
                self.message_success,
            )
        success_url = self.request.POST.get('next', None)
        if success_url is not None:
            return success_url
        else:
            return settings.REDIRECT_URL


class OwnershipCheck(object):
    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update notes """
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponseNotFound(
                _('Rezo is not hacked. You don\'t have the permission xD')
            )
        return super(OwnershipCheck, self).dispatch(request, *args, **kwargs)


class NoteCreateView(MessageRedirect, generic.CreateView):
    model = Note
    fields = ('message', )
    message_success = _(
        """Your note has been added to the board, """
        """it will be displayed in a moment"""
    )
    template_name = 'shoutbox/message/form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NoteCreateView, self).form_valid(form)


class NoteEditView(MessageRedirect, OwnershipCheck, generic.UpdateView):
    model = Note
    fields = ('message', )
    template_name = 'shoutbox/message/form.html'
    message_success = _(
        'Your note has been updated, it will be refreshed in a moment'
    )


class NoteDeleteView(MessageRedirect, OwnershipCheck, generic.DeleteView):
    model = Note
    template_name = 'shoutbox/note_confirm_delete.html'
    message_success = _(
        'Your note has been removed, it will be refreshed in a moment'
    )
