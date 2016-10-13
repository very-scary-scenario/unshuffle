from django import forms


class GameForm(forms.Form):
    card_id = forms.CharField()
    index = forms.IntegerField()
