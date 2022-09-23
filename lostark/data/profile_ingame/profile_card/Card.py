class Card:
    def __init__(self, name, index, grade, item_data, src):
        self.__name = name
        self.__index = index
        self.__grade = grade
        self.__item_data = item_data
        self.__src = src

    def __str__(self):
        return "{} {}".format(self.name, self.src)

    @property
    def name(self):
        return self.__name

    @property
    def index(self):
        return self.__index

    @property
    def grade(self):
        return self.__grade

    @property
    def item_data(self):
        return self.__item_data

    @property
    def src(self):
        return self.__src


class CardEffect:
    def __init__(self, index, title, description):
        self.__index = index
        self.__title = title
        self.__description = description

    def __str__(self):
        return "{}: {}".format(self.title, self.description)

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def index(self):
        return self.__index
