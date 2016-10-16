from random import shuffle

from camel import CamelRegistry

reg = CamelRegistry()


class Loadable(object):
    def __init__(self, **attrs):
        super().__init__()

        for attr in self.persistent_attrs:
            setattr(self, attr, None)

        for k, v in attrs.items():
            if k not in self.persistent_attrs:
                raise ValueError('{} is not persistent'.format(k))

            setattr(self, k, v)

    def dump(self):
        return {attr: getattr(self, attr) for attr in self.persistent_attrs}


class Game(Loadable):
    persistent_attrs = {
        'river', 'deck_name', 'deck', 'players', 'round', 'turn',
        'base_hand_size', 'initial_river_size', 'discard_incorrect_plays',
    }

    @property
    def started(self):
        return bool(self.deck)

    def start(
        self, source, players=None,
        base_hand_size=3,
        initial_river_size=1,
        discard_incorrect_plays=True,
    ):
        self.base_hand_size = base_hand_size
        self.initial_river_size = initial_river_size
        self.discard_incorrect_plays = discard_incorrect_plays

        self.deck_name = source.deck_name
        self.deck = list(source())

        shuffle(self.deck)

        self.players = players or self.players or None

        if self.players is None:
            raise ValueError('game started with no players')

        self.deal()

    def sort_river(self):
        self.river.sort(key=lambda o: o['order'])

    def next_card(self):
        return self.deck.pop()

    def deal(self):
        self.river = []

        for i in range(self.base_hand_size):
            for player in self.players:
                player.hand.append(self.next_card())

        for i in range(self.initial_river_size):
            self.river.append(self.next_card())

        self.sort_river()

    def play(self, player, hand_index, river_index):
        self.river.insert(river_index, player.hand.pop(hand_index))
        frame = self.river[max(0, river_index-1):river_index+2]

        previous_card = frame[0]
        for card in frame[1:]:
            if card['order'] < previous_card['order']:
                correct = False
                player.hand.append(self.next_card())

                if self.discard_incorrect_plays:
                    self.river.pop(river_index)
                else:
                    self.sort_river()

                break

            previous_card = card
        else:
            correct = True

        return correct

    def save(self):
        pass


class Player(Loadable):
    persistent_attrs = {'hand', 'name'}

    @classmethod
    def new(cls, name):
        player = cls()

        player.name = name
        player.hand = []

        return player


@reg.loader('game', version=1)
def _load_game(data, version):
    return Game(**data)


@reg.dumper(Game, 'game', version=1)
def _dump_game(game):
    return game.dump()


@reg.loader('player', version=1)
def _load_player(data, version):
    return Player(**data)


@reg.dumper(Player, 'player', version=1)
def _dump_player(player):
    return player.dump()
