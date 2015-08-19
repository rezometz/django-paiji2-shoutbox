from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound
from django.utils.translation import ugettext as _

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


class NoteCreateView(generic.CreateView):
    model = Note
    fields = ('message', )
    message_create = _(
        """Your note has been added to the board, """
        """it will be displayed in a moment"""
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NoteCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(
            self.request,
            self.message_create,
        )
        success_url = self.request.POST.get('next')
        return success_url if success_url is not None else reverse('index')


class NoteEditView(generic.UpdateView):
    model = Note
    fields = ('message', )
    template_name = 'shoutbox/note_form.html'

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update notes """
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponseNotFound(
                _('Rezo is not hacked. You don\'t have the permission xD')
            )
        return super(NoteEditView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(
            self.request,
            _('Your note has been updated, it will be refreshed in a moment'),
        )
        success_url = self.request.POST.get('next')
        return success_url if success_url is not None else reverse('index')


class NoteDeleteView(generic.DeleteView):
    model = Note
    template_name = 'shoutbox/note_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update notes """
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponseNotFound(
                _('Rezo is not hacked. You don\'t have the permission xD')
            )
        return super(NoteDeleteView, self).dispatch(
            request, *args, **kwargs
        )

    def get_success_url(self):
        messages.success(
            self.request,
            _('Your note has been removed, it will be refreshed in a moment'),
        )
        success_url = self.request.POST.get('next')
        return success_url if success_url is not None else reverse('index')
