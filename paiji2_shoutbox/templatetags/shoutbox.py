from django import template
from django.core.urlresolvers import reverse

from ..models import Note
from ..forms import BlockNoteForm


register = template.Library()


@register.inclusion_tag(
    'shoutbox/bulletin_board_short.html',
    takes_context=True,
)
def display_bulletin_board(context, nb=5):
    return {
        'request': context['request'],
        'notes': Note.objects.select_related('author').all()[:nb],
        'form': BlockNoteForm(),
        'message_add': reverse('message-add'),
    }
