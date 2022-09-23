class SpecialItem:
    def __init__(self, name, src, color):
        self.__name = name
        self.__src = src
        self.__color = color

    def __str__(self):
        return "{} {} {}".format(self.name, self.color, self.src)

    @property
    def name(self):
        return self.__name

    @property
    def color(self):
        return self.__color

    @property
    def src(self):
        return self.__src
