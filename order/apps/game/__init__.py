from copy import copy
from random import shuffle

from camel import CamelRegistry

reg = CamelRegistry()


class NaiveLoadable(object):
    def __init__(self, **attrs):
        super().__init__()

        for k, v in attrs.items():
            setattr(self, k, v)


class Game(NaiveLoadable):
    @classmethod
    def new(cls, objects, sort_by, title_by, players):
        game = cls()

        game.base_hand_size = 3
        game.objects = list(sorted(objects, key=lambda o: o[sort_by]))
        game.title_by = title_by
        game.players = players
        game.deal()

        return game

    def next_card(self):
        return self.deck.pop()

    def deal(self):
        self.deck = copy(self.objects)
        shuffle(self.deck)

        self.river = []

        for i in range(self.base_hand_size):
            for player in self.players:
                player.hand.append(self.next_card())

        self.river.append(self.next_card())

    def save(self):
        pass


class Player(NaiveLoadable):
    @classmethod
    def new(cls):
        player = cls()

        player.name = 'colons'
        player.hand = []

        return player


@reg.loader('game', version=1)
def _load_game(data, version):
    return Game(**data)


@reg.dumper(Game, 'game', version=1)
def _dump_game(game):
    return {
        'objects': game.objects,
        'river': game.river,
        'deck': game.deck,
        'players': game.players,
    }


@reg.loader('player', version=1)
def _load_player(data, version):
    return Player(**data)


@reg.dumper(Player, 'player', version=1)
def _dump_player(player):
    return {
        'hand': player.hand,
        'name': player.name,
    }
