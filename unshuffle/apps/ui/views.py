from camel import Camel
from classtools import reify

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, FormView

from .forms import GameForm, JoinGameForm, ConfigureGameForm
from .models import Game as GameStore
from ..game import reg, Game, Player
from ..sources import SOURCES


camel = Camel([reg])


class StartGameView(FormView):
    template_name = 'index.html'
    form_class = JoinGameForm

    def form_valid(self, form):
        game_store, created = GameStore.objects.get_or_create(
            name=form.cleaned_data['game_name'],
        )

        game = camel.load(game_store.state) or Game(players=[])

        if not game.started:
            game.players.append(Player.new(form.cleaned_data['your_name']))
            game_store.state = camel.dump(game)
            game_store.save()

        self.request.session[game_store.name] = (
            form.cleaned_data['your_name']
        )

        return redirect(game_store.get_absolute_url())


class GameMixin(object):
    @reify
    def player_name(self):
        return self.request.session.get(self.game._store.name, None)

    @reify
    def player(self):
        player, = (p for p in self.game.players if self.player_name == p.name)
        return player

    def save_game(self):
        self.game._store.state = camel.dump(self.game)
        self.game._store.save()

    @reify
    def game(self):
        game_store = get_object_or_404(GameStore, name=self.kwargs['name'])
        game = camel.load(game_store.state)
        game._store = game_store
        return game

    def get_context_data(self, *a, **k):
        return {
            **super().get_context_data(*a, **k),
            'game': self.game,
            'player': self.player,
        }


class ConfigureGameView(GameMixin, FormView):
    template_name = 'configure.html'
    form_class = ConfigureGameForm
    success_url = '.'

    def form_valid(self, form):
        self.game.start(SOURCES[form.cleaned_data['deck']])
        self.save_game()
        return super().form_valid(form)


class AwaitView(GameMixin, TemplateView):
    template_name = 'await.html'


class GameView(GameMixin, FormView):
    form_class = GameForm
    template_name = 'game.html'
    success_url = '.'

    def dispatch(self, *a, **k):
        if self.game.started:
            return super().dispatch(*a, **k)

        if self.player_name == self.game.players[0].name:
            return ConfigureGameView.as_view()(*a, **k)

        if self.player_name:
            return AwaitView.as_view()(*a, **k)

        return redirect(reverse('index'))

    def get_form(self, *a, **k):
        form = super().get_form(*a, **k)
        form.game = self.game
        form.player = self.player
        return form

    def form_valid(self, form):
        self.game.play(
            self.player, form.cleaned_data['card'], form.cleaned_data['index'],
        )
        self.save_game()

        return super().form_valid(form)
