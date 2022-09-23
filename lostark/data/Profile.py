from lostark.data.profile_character_list import ProfileCharacter
from lostark.data.profile_ingame import ProfileIngame
from lostark.util import *


class Profile:
    def __init__(self, bs_object):
        self.__lv = bs_object.body.find("span", {"class": "profile-character-info__lv"}).text.strip()
        self.__name = bs_object.body.find("span", {"class": "profile-character-info__name"}).text.strip()
        self.__server = bs_object.body.find("span", {"class": "profile-character-info__server"}).text.strip()

        # character list
        profile_character_list = bs_object.body.find("div", {"class": "profile-character-list"})
        self.__profile_character_list = ProfileCharacter(get_bs_object(profile_character_list))

        # profile-ingame
        profile_ingame = bs_object.body.find("div", {"class": "profile-ingame"})
        self.__profile_ingame = ProfileIngame(get_bs_object(profile_ingame))

    def __str__(self):
        return '{} {} {}\n\n{}\n{}\n' \
            .format(self.lv, self.name, self.server, self.profile_character_list, self.profile_ingame)

    @property
    def lv(self):
        return self.__lv

    @property
    def name(self):
        return self.__name

    @property
    def server(self):
        return self.__server

    @property
    def profile_character_list(self):
        return self.__profile_character_list

    @property
    def profile_ingame(self):
        return self.__profile_ingame
