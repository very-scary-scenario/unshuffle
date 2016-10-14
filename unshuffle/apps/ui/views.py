import os

from camel import Camel
from classtools import reify

from django.views.generic import FormView

from .forms import GameForm
from ..game import reg, Game, Player
from ..sources import veekun


GAMEFILE = 'game.yaml'


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
        if not os.path.exists(GAMEFILE):
            print('making a new game')
            game = Game.new(veekun.load(),
                            'identifier', 'identifier', [Player.new()])

            with open(GAMEFILE, 'w') as gf:
                gf.write(Camel([reg]).dump(game))

        with open(GAMEFILE) as gf:
            return Camel([reg]).load(gf.read())

    def form_valid(self, form):
        correct = self.game.play(
            self.player, form.cleaned_data['card'], form.cleaned_data['index'],
        )

        print('correct: {}'.format(correct))

        with open(GAMEFILE, 'w') as gf:
            gf.write(Camel([reg]).dump(self.game))

        return super().form_valid(form)

    def get_context_data(self, *a, **k):
        return {
            **super().get_context_data(*a, **k),
            'game': self.game,
        }
