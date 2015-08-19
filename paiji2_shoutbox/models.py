from django.db import models
from django.utils.translation import ugettext as _
from django.utils.timezone import now


try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except:
    from django.contrib.auth.models import User


class Note(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name=_('author'),
        related_name='notes',
    )
    message = models.CharField(
        _('message'),
        max_length=200,
    )
    posted_at = models.DateTimeField(
        _('publication date'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('note')
        verbose_name_plural = _('notes')
        ordering = ('-posted_at', )
