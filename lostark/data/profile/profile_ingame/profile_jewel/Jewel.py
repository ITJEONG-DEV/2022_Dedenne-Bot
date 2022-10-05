class Jewel:
    def __init__(self, jewel_id, name, info, lv, grade, equip_data, equip_src, effect_data, effect_src, skill_name, effect):
        self.__id = jewel_id

        self.__name = name

        self.__info = info
        self.__lv = lv
        self.__grade = grade

        self.__equip_data = equip_data
        self.__equip_src = equip_src

        self.__effect_data = effect_data
        self.__effect_src = effect_src
        self.__skill_name = skill_name
        self.__effect = effect

    def __str__(self):
        return "{} {} {}, {} {}" \
            .format(self.name, self.info, self.lv, self.skill_name, self.effect)

    @property
    def jewel_id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def info(self):
        return self.__info

    @property
    def lv(self):
        return self.__lv

    @property
    def grade(self):
        return self.__grade

    @property
    def equip_data(self):
        return self.__equip_data

    @property
    def equip_src(self):
        return self.__equip_src

    @property
    def effect_data(self):
        return self.__effect_data

    @property
    def effect_src(self):
        return self.__effect_src

    @property
    def skill_name(self):
        return self.__skill_name

    @property
    def effect(self):
        return self.__effect
