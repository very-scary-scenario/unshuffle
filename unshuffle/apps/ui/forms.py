from django import forms

from ..sources import SOURCES


class JoinGameForm(forms.Form):
    your_name = forms.CharField()
    game_name = forms.SlugField()


class ConfigureGameForm(forms.Form):
    deck = forms.ChoiceField(choices=list(sorted(
        (category_name, list(sorted((
            ('{}::{}'.format(category_name, k), k)
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
