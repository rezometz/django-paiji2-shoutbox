from django.forms import ModelForm, TextInput
from models import Note


class NoteForm(ModelForm):

    class Meta:
        model = Note
        fields = ['message']


class BlockNoteForm(NoteForm):

    class Meta:
        model = Note
        fields = ['message']
        widgets = {
            'message': TextInput(attrs={'id': 'id_block_note'})
        }
