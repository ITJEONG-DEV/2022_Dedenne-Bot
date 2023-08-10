class SetEffect:
    def __init__(self, set_name, name, lv, effect):
        self.set_name = set_name
        self.name = name
        self.lv = lv
        self.effect = effect


class SetEffects:
    def __init__(self):
        self.effects = []

    def add(self, set_name, name, lv, effect):
        self.effects.append(SetEffect(set_name, name, lv, effect))
