from django.contrib import admin

from paiji2_shoutbox.models import Note


class ShoutboxAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'message',
        'posted_at',
    )


admin.site.register(Note, ShoutboxAdmin)
