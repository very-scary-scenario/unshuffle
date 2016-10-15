from django import forms

from ..sources import SOURCES


class JoinGameForm(forms.Form):
    your_name = forms.CharField()
    game_name = forms.SlugField()


class ConfigureGameForm(forms.Form):
    deck = forms.ChoiceField(choices=list(sorted((
        (k, k) for k in SOURCES.keys()
    ))))


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
