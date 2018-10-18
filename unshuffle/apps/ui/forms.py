from django import forms
from django.core.exceptions import ValidationError

from .models import Room
from ..sources import SOURCES


SOURCE_SEP = '::'


class JoinGameForm(forms.Form):
    your_name = forms.CharField(required=True)
    room_code = forms.SlugField(help_text="Leave blank to start a new game",
                                required=False)

    def clean_room_code(self):
        if self.data['room_code']:
            try:
                return Room.objects.recently_active().get(
                    code=self.data['room_code'])
            except Room.DoesNotExist:
                raise ValidationError('No room found with that code')
        else:
            return ''


class ConfigureGameForm(forms.Form):
    deck = forms.ChoiceField(choices=list(sorted(
        (category_name, list(sorted((
            ('{}{}{}'.format(category_name, SOURCE_SEP, k), k)
            for k in category.keys()
        )))) for category_name, category in SOURCES.items())
    ))
    base_hand_size = forms.IntegerField(
        initial=3, min_value=1, max_value=10,
    )
    initial_river_size = forms.IntegerField(
        initial=1, min_value=1, max_value=10,
    )
    discard_incorrect_plays = forms.BooleanField(initial=True)


class GameForm(forms.Form):
    card = forms.IntegerField(min_value=0)
    index = forms.IntegerField(min_value=0)

    def clean_index(self):
        index = self.cleaned_data['index']

        if not (0 <= index <= len(self.game.river)):
            raise forms.ValidationError('invalid index')

        return index

    def clean_card(self):
        index = self.cleaned_data['card']

        if not (0 <= index <= len(self.player.hand)):
            raise forms.ValidationError('invalid index')

        return index
