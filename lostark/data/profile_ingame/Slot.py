class Slot:
    def __init__(self, class_name, grade, item, src):
        self.__class = class_name
        self.__grade = grade
        self.__item = item
        self.__src = src

    def __str__(self):
        return "{}, {}, {}, {}".format(self.class_name, self.item, self.grade, self.src)

    @property
    def grade(self):
        return self.__grade

    @property
    def item(self):
        return self.__item

    @property
    def src(self):
        return self.__src

    @property
    def class_name(self):
        return self.__class
