class ProfileAbilityEngrave:
    def __init__(self):
        self.__ability = []
        self.__effect = []

    def __str__(self):
        s = "\n각인\n"
        for i in range(len(self.__ability)):
            s += str(self.__ability[i]) + ": " + str(self.__effect[i]) + "\n"

        return s

    @property
    def ability(self):
        return self.__ability

    @property
    def effect(self):
        return self.__effect

    def add_ability(self, ability, effect):
        self.__ability.append(ability)
        self.__effect.append(effect)
