from lostark.data.profile_ingame import SpecialItem
from lostark.util import *


class ProfileInfo:
    def __init__(self, bs_object: BeautifulSoup):
        self.__expedition_lv = ""
        self.__battle_lv = ""

        self.__equip_item_lv = ""
        self.__achieve_item_lv = ""

        self.__title = ""
        self.__guild = ""
        self.__pvp_level = ""

        self.__estate_name = ""
        self.__estate_lv = ""

        self.__items = []

        self.__parse__(bs_object)

    def __str__(self):
        s1 = "원정대 {}, 전투 {}\n장착 아이템 {}, 달성 아이템 {}\n칭호 {}, 길드 {}, PVP {}, 영지 {}, {}\n\n" \
            .format(self.expedition_lv, self.battle_lv, self.equip_item_lv, self.achieve_item_lv, self.title,
                    self.guild, self.pvp_lv, self.estate_name, self.estate_lv)

        s2 = "특수장비\n"
        for item in self.special_items:
            s2 += str(item) + "\n\n"

        return s1 + s2

    def __parse__(self, bs_object: BeautifulSoup):
        expedition = bs_object.find("div", {"class": "level-info__expedition"})
        contents = get_bs_object(expedition).findAll("span")[-1].text
        self.__expedition_lv = contents

        battle = bs_object.find("div", {"class": "level-info__item"})
        contents = get_bs_object(battle).findAll("span")[-1].text
        self.__battle_lv = contents

        equip_item = bs_object.find("div", {"class": "level-info2__expedition"})
        contents = get_bs_object(equip_item).findAll("span")[-1].text
        self.__equip_item_lv = contents

        achieve_item = bs_object.find("div", {"class": "level-info2__item"})
        contents = get_bs_object(achieve_item).findAll("span")[-1].text
        self.__achieve_item_lv = contents

        title = bs_object.find("div", {"class": "game-info__title"})
        contents = get_bs_object(title).findAll("span")[-1].text
        self.__title = contents

        guild = bs_object.find("div", {"class": "game-info__guild"})
        contents = get_bs_object(guild).findAll("span")[-1].text
        self.__guild = contents

        pvp = bs_object.find("div", {"class": "level-info__pvp"})
        contents = get_bs_object(pvp).findAll("span")[-1].text
        self.__pvp_level = contents

        estate = bs_object.find("div", {"class": "game-info__wisdom"})
        contents = get_bs_object(estate).findAll("span")
        self.__estate_lv = contents[1].text
        self.__estate_name = contents[-1].text

        special_info = bs_object.find("div", {"special-info__item"})
        item_slot = get_bs_object(special_info).findAll("li")

        for i in range(len(item_slot)):
            item = get_bs_object(item_slot[i])

            img = get_bs_object(item.findAll("div")[1]).img
            if img is None:
                continue

            src = img["src"]
            name = item.find("span").text
            color = item.find("font")["color"]

            self._add_special_item(src, name, color)

    def _add_special_item(self, src, name, color):
        self.__items.append(SpecialItem(name=name, color=color, src=src))

    @property
    def expedition_lv(self):
        return self.__expedition_lv

    @property
    def battle_lv(self):
        return self.__battle_lv

    @property
    def equip_item_lv(self):
        return self.__equip_item_lv

    @property
    def achieve_item_lv(self):
        return self.__achieve_item_lv

    @property
    def title(self):
        return self.__title

    @property
    def guild(self):
        return self.__guild

    @property
    def pvp_lv(self):
        return self.__pvp_level

    @property
    def estate_name(self):
        return self.__estate_name

    @property
    def estate_lv(self):
        return self.__estate_lv

    @property
    def special_items(self):
        return self.__items
