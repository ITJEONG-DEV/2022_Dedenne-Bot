from lostark.util import *
from . import ProfileSkillLife


class ProfileStability:
    def __init__(self, bs_object: BeautifulSoup):

        # profile skill life
        self.__profile_skill_life = ProfileSkillLife()
        ul = bs_object.find("ul", {"class": "profile-skill-life__list"})
        life_skill_list = get_bs_object(ul).findAll("li")

        for li in life_skill_list:
            life_skill = " L".join(li.text.split("L"))
            self.__profile_skill_life.add(life_skill)


    def __str__(self):
        return f"{self.profile_skill_life}"

    @property
    def profile_skill_life(self):
        return self.__profile_skill_life
