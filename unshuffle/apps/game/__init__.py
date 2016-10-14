from random import shuffle

from camel import CamelRegistry

reg = CamelRegistry()


class Loadable(object):
    def __init__(self, **attrs):
        super().__init__()

        for k, v in attrs.items():
            if k not in self.persistent_attrs:
                raise ValueError('{} is not persistent, ignoring'.format(k))

            setattr(self, k, v)

    def dump(self):
        return {attr: getattr(self, attr) for attr in self.persistent_attrs}


class Game(Loadable):
    persistent_attrs = {'river', 'deck', 'sort_by', 'title_by', 'players'}

    @classmethod
    def new(cls, objects, sort_by, title_by, players):
        game = cls()

        game.base_hand_size = 3

        game.deck = list(objects)
        shuffle(game.deck)

        game.sort_by = sort_by
        game.title_by = title_by
        game.players = players
        game.deal()

        return game

    def sort_river(self):
        self.river.sort(key=lambda o: o[self.sort_by])

    def next_card(self):
        return self.deck.pop()

    def deal(self):
        self.river = []

        for i in range(self.base_hand_size):
            for player in self.players:
                player.hand.append(self.next_card())

        self.river.append(self.next_card())

    def play(self, player, hand_index, river_index):
        self.river.insert(river_index, player.hand.pop(hand_index))
        frame = self.river[max(0, river_index-1):river_index+2]
        print(frame)

        previous_card = frame[0]
        for card in frame[1:]:
            if card[self.sort_by] < previous_card[self.sort_by]:
                correct = False
                player.hand.append(self.next_card())
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
    return game.dump()


@reg.loader('player', version=1)
def _load_player(data, version):
    return Player(**data)


@reg.dumper(Player, 'player', version=1)
def _dump_player(player):
    return player.dump()
