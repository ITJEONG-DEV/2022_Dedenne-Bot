class ProfileState:
    def __init__(self):
        self.__value = []

        self.__intellect = 0
        self.__courage = 0
        self.__charm = 0
        self.__kindness = 0

    def __str__(self):
        s = "\n성향\n"
        s += f"지성: {self.intellect}\n담력: {self.courage}\n"
        s += f"매력: {self.charm}\n친절: {self.kindness}\n"

        return s

    @property
    def intellect(self):
        return self.__intellect

    @intellect.setter
    def intellect(self, value):
        self.__intellect = value

    @property
    def courage(self):
        return self.__courage

    @courage.setter
    def courage(self, value):
        self.__courage = value

    @property
    def charm(self):
        return self.__charm

    @charm.setter
    def charm(self, value):
        self.__charm = value

    @property
    def kindness(self):
        return self.__kindness

    @kindness.setter
    def kindness(self, value):
        self.__kindness = value

    def set_state(self, value):
        self.intellect = value[0]
        self.courage = value[1]
        self.charm = value[2]
        self.kindness = value[3]
