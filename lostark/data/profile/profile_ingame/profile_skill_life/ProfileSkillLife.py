class ProfileSkillLife:
    def __init__(self):
        self.__skill = []

    def __str__(self):
        s = "\n생활스킬\n"
        for skill in self.skill:
            s += skill + "\n"

        return s

    @property
    def skill(self):
        return self.__skill

    def add(self, item):
        self.__skill.append(item)
