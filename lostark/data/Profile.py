import re
import json

from lostark.data.profile_character_list import ProfileCharacter
from lostark.data.profile_ingame import ProfileIngame
from . import CharacterState, ProfileState
from lostark.util import *


class Profile:
    def __init__(self, bs_object):
        self.__lv = bs_object.body.find("span", {"class": "profile-character-info__lv"}).text.strip()
        self.__name = bs_object.body.find("span", {"class": "profile-character-info__name"}).text.strip()
        self.__server = bs_object.body.find("span", {"class": "profile-character-info__server"}).text.strip()[1:]
        self.__emblem = bs_object.body.find("img", {"class": "profile-character-info__img"})["src"]

        self.__state = CharacterState(bs_object)

        # character list
        profile_character_list = bs_object.body.find("div", {"class": "profile-character-list"})
        self.__profile_character_list = ProfileCharacter(get_bs_object(profile_character_list))

        # profile-ingame
        profile_ingame = bs_object.body.find("div", {"class": "profile-ingame"})
        self.__profile_ingame = ProfileIngame(get_bs_object(profile_ingame))

        # profile-state
        scripts = bs_object.findAll("script", {"type": "text/javascript"})
        self.__profile_state = ProfileState()

        for script in scripts:
            if "#chart-states" in script.text:
                contents = script.text

                matched = re.search(r'lui.profile.StatesGraph(.*?);', contents, re.S)

                content = matched.group(1)

                words = content.split()

                intellect = int(words[5][1:-1])
                courage = int(words[6][:-1])
                charm = int(words[7][:-1])
                kindness = int(words[8][:-2])

                self.__profile_state.intellect = intellect
                self.__profile_state.courage = courage
                self.__profile_state.charm = charm
                self.__profile_state.kindness = kindness

    def __str__(self):
        return '{} {} {} {} {}\n\n{}\n{}\n{}\n' \
            .format(self.lv, self.name, self.server, self.emblem, self.state, self.profile_character_list,
                    self.profile_ingame, self.profile_state)

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
    def emblem(self):
        return self.__emblem

    @property
    def state(self):
        return self.__state

    @property
    def profile_character_list(self):
        return self.__profile_character_list

    @property
    def profile_ingame(self):
        return self.__profile_ingame

    @property
    def profile_state(self):
        return self.__profile_state
