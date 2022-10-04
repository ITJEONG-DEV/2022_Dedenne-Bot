from lostark.data.profile_ingame import *
from lostark.util import *


class ProfileIngame:
    def __init__(self, bs_object: BeautifulSoup):
        self.__profile_info = None
        self.__parse__(bs_object)

    def __str__(self):
        return str(self.profile_info) + str(self.profile_equipment)

    def __parse__(self, bs_object: BeautifulSoup):
        self.__profile_info = ProfileInfo(bs_object)

        self.__profile_equipment = ProfileEquipment(bs_object)

    @property
    def profile_info(self):
        return self.__profile_info

    @property
    def profile_equipment(self):
        return self.__profile_equipment

