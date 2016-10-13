import os

from camel import Camel
from classtools import reify

from django.views.generic import FormView

from .forms import GameForm
from ..game import reg, Game, Player
from ..sources import veekun


class GameView(FormView):
    form_class = GameForm
    template_name = 'game.html'

    @reify
    def game(self):
        if not os.path.exists('game.yml'):
            game = Game.new(veekun.load(),
                            'species_id', 'identifier', [Player.new()])

            with open('game.yaml', 'w') as gf:
                gf.write(Camel([reg]).dump(game))

        with open('game.yaml') as gf:
            return Camel([reg]).load(gf.read())

    def get_context_data(self):
        return {
            **super().get_context_data(),
            'game': self.game,
        }
