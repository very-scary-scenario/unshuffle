from camel import Camel
from classtools import reify

from django.views.generic import FormView

from .forms import GameForm
from .models import Game as GameStore
from ..game import reg, Game, Player
from ..sources import veekun


class GameView(FormView):
    form_class = GameForm
    template_name = 'game.html'
    success_url = '.'

    def get_form(self, *a, **k):
        form = super().get_form(*a, **k)
        form.game = self.game
        form.player = self.player
        return form

    @reify
    def player(self):
        return self.game.players[0]

    @reify
    def game(self):
        game_store, created = GameStore.objects.get_or_create(
            name=self.kwargs['name'],
        )

        if created:
            game = Game.new(veekun.load(),
                            'identifier', 'identifier', [Player.new()])

            game_store.state = Camel([reg]).dump(game)
            game_store.save()
            return game

        return Camel([reg]).load(game_store.state)

    def form_valid(self, form):
        self.game.play(
            self.player, form.cleaned_data['card'], form.cleaned_data['index'],
        )

        GameStore.objects.filter(name=self.kwargs['name']).update(
            state=Camel([reg]).dump(self.game)
        )

        return super().form_valid(form)

    def get_context_data(self, *a, **k):
        return {
            **super().get_context_data(*a, **k),
            'game': self.game,
        }
