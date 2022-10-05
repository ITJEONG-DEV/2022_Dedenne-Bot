import requests

from . import ProfileCollection
from lostark.util import *
from lostark.data.profile.profile_ingame import ProfileSkillLife
from lostark.data.profile import Info


class ProfileStability:
    def __init__(self, bs_object: BeautifulSoup, info: Info):
        # profile skill life
        self.__profile_skill_life = ProfileSkillLife()
        ul = bs_object.find("ul", {"class": "profile-skill-life__list"})
        life_skill_list = get_bs_object(ul).findAll("li")

        for li in life_skill_list:
            life_skill = " L".join(li.text.split("L"))
            self.__profile_skill_life.add(life_skill)

        # get collection
        self.__profile_collection = None
        url = "https://lostark.game.onstove.com/Profile/GetCollection?" + \
              f"memberNo={info.member_no}&worldNo={info.world_no}&pcId={info.pc_id}"

        response = requests.get(url)
        if response.text is not None:
            self.__profile_collection = ProfileCollection(get_bs_object(response.text))

    def __str__(self):
        return f"{self.profile_skill_life}\n{self.__profile_collection}\n"

    @property
    def profile_skill_life(self):
        return self.__profile_skill_life

    @property
    def profile_collection(self):
        return self.__profile_collection
