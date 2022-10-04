from lostark.util import *


class CharacterState:
    def __init__(self, bs_object):
        profile_ability_basic = bs_object.find("div", {"class": "profile-ability-basic"})
        all_span = get_bs_object(profile_ability_basic).findAll("span")

        if len(all_span) == 0:
            self.__attack = 0
            self.__hp = 0

        else:
            self.__attack = all_span[1].text
            self.__hp = all_span[3].text

        profile_ability_battle = bs_object.find("div", {"class": "profile-ability-battle"})
        all_span = get_bs_object(profile_ability_battle).findAll("span")

        if len(all_span) == 0:
            self.__fatal = 0
            self.__specialization = 0
            self.__overpowering = 0
            self.__swiftness = 0
            self.__patience = 0
            self.__skilled = 0

        else:
            # 치명
            self.__fatal = all_span[1].text
            # 특화
            self.__specialization = all_span[3].text
            # 제압
            self.__overpowering = all_span[5].text
            # 신속
            self.__swiftness = all_span[7].text
            # 인내
            self.__patience = all_span[9].text
            # 숙련
            self.__skilled = all_span[11].text

    def __str__(self):
        return f"attack: {self.attack}\nhp: {self.hp}\n" + \
               f"치명: {self.fatal} 특화: {self.specialization} 제압: {self.overpowering}" + \
               f"신속: {self.swiftness} 인내: {self.patience} 숙련: {self.skilled}"

    @property
    def attack(self):
        return self.__attack

    @property
    def hp(self):
        return self.__hp

    # 치명
    @property
    def fatal(self):
        return self.__fatal

    # 특화
    @property
    def specialization(self):
        return self.__specialization

    # 제압
    @property
    def overpowering(self):
        return self.__overpowering

    # 신속
    @property
    def swiftness(self):
        return self.__swiftness

    # 인내
    @property
    def patience(self):
        return self.__patience

    # 숙련
    @property
    def skilled(self):
        return self.__skilled
