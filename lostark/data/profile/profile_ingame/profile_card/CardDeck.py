from . import Card, CardEffect


class CardDeck:
    def __init__(self):
        self.__effect = []
        self.__cards = []

    def __str__(self):
        s = "\n카드\n"
        for card in self.__cards:
            s += str(card) + "\n"

        s += "\n세트효과\n"
        for effect in self.__effect:
            s += str(effect) + "\n"

        return s

    @property
    def cards(self):
        return self.__cards

    @property
    def effect(self):
        return self.__effect

    def add_card(self, card: Card):
        self.__cards.append(card)

    def add_effect(self, effect: CardEffect):
        self.__effect.append(effect)