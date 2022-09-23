from lostark.data.profile_ingame import Slot, Jewel
from lostark.util import *


class ProfileEquipment:
    def __init__(self, bs_object: BeautifulSoup):
        self.__src = ""

        self.__equipment_slot = []
        self.__avatar_slot = []
        self.__jewel_slot = []
        self.__card_slot = []

        self.__parse__(bs_object)

    def __str__(self):
        s = self.src + "\n"

        s += "\n착용 장비\n"
        for slot in self.__equipment_slot:
            s += str(slot) + "\n"

        s += "\n아바타\n"
        for slot in self.__avatar_slot:
            s += str(slot) + "\n"

        s += "\n보석\n"
        for slot in self.__jewel_slot:
            s += str(slot) + "\n"

        s += "\n카드\n"
        for slot in self.__card_slot:
            s += str(slot) + "\n"

        return s

    def __parse_profile_equipment_character__(self, bs_object: BeautifulSoup):
        profile_equipment_character = bs_object.find("div", {"class": "profile-equipment__character"})
        img = get_bs_object(profile_equipment_character).img
        self.__src = img["src"]

    def __parse_profile_equipment_slot__(self, bs_object: BeautifulSoup):
        profile_equipment_slot = bs_object.find("div", {"class": "profile-equipment__slot"})
        equipment_slot = get_bs_object(profile_equipment_slot).findAll("div")

        for i in range(len(equipment_slot)):
            slot = get_bs_object(equipment_slot[i]).div
            class_name = slot["class"][0]

            if "profile" in class_name:
                continue

            item_data = slot["data-item"]
            grade = slot["data-grade"]

            img = get_bs_object(slot).img
            src = img["src"]

            self.__equipment_slot.append(Slot(
                class_name=class_name,
                grade=grade,
                item=item_data,
                src=src
            ))

    def __parse_profile_avatar_slot__(self, bs_object: BeautifulSoup):
        profile_avatar_slot = bs_object.find("div", {"class": "profile-avatar__slot"})
        avatar_slot = get_bs_object(profile_avatar_slot).findAll("div")

        for i in range(len(avatar_slot)):
            slot = get_bs_object(avatar_slot[i]).div
            class_name = slot["class"][0]

            if "profile" in class_name:
                continue

            grade = slot["data-grade"]

            if grade == "":
                continue

            item_data = slot["data-item"]

            img = get_bs_object(slot).img
            src = img["src"]

            self.__avatar_slot.append(Slot(
                class_name=class_name,
                grade=grade,
                item=item_data,
                src=src
            ))

    def __parse_profile_jewel_slot__(self, bs_object: BeautifulSoup):
        profile_jewel_slot = bs_object.find("div", {"class": "jewel-effect__wrap"})

        jewel_wrap = get_bs_object(profile_jewel_slot).find("div", {"class": "jewel__wrap"})
        jewel_span_list = get_bs_object(jewel_wrap).findAll("span")

        jewel_effect = get_bs_object(profile_jewel_slot).find("div", {"class": "box_wrapper"})
        jewel_effect_list = get_bs_object(jewel_effect).findAll("li")

        current_jewel = []
        for i in range(len(jewel_span_list)):
            span = get_bs_object(jewel_span_list[i]).span
            class_name = span["class"][0]

            if class_name == "jewel_btn":
                spans = get_bs_object(span).findAll("span")

                jewel = {
                    "grade": span["data-grade"],
                    "item_data": span["data-item"],
                    "id": span["id"]
                }

                for item in spans:
                    temp = get_bs_object(item).span
                    tag = temp["class"][0]

                    if tag == "info":
                        jewel["info"] = temp.text

                    elif tag == "jewel_img":
                        img = get_bs_object(temp).img
                        jewel["src"] = img["src"]

                    elif tag == "jewel_level":
                        jewel["lv"] = temp.text

                if len(jewel.keys()) != 0:
                    current_jewel.append(jewel)

        current_effect = []
        for i in range(len(jewel_effect_list)):
            item = get_bs_object(jewel_effect_list[i])

            slot = item.find("span")
            img = get_bs_object(slot).img

            jewel = {
                "id": slot["data-gemkey"],
                "item_data": slot["data-item"],
                "src": img["src"],
            }

            skill_name = item.find("strong", {"class": "skill_tit"}).text
            effect = item.find("p", {"class": "skill_detail"}).text[len(skill_name) + 1:]

            jewel["skill_name"] = skill_name
            jewel["effect"] = effect

            current_effect.append(jewel)

        for i in range(len(current_jewel)):
            for j in range(len(current_effect)):
                if current_jewel[i]["id"] == current_effect[j]["id"]:
                    jewel = Jewel(
                        jewel_id=current_jewel[i]["id"],

                        info=current_jewel[i]["info"],
                        lv=current_jewel[i]["lv"],
                        grade=current_jewel[i]["grade"],

                        equip_data=current_jewel[i]["item_data"],
                        equip_src=current_jewel[i]["src"],

                        effect_data=current_effect[j]["item_data"],
                        effect_src=current_effect[j]["src"],

                        skill_name=current_effect[j]["skill_name"],
                        effect=current_effect[j]["effect"]
                    )
                    self.__jewel_slot.append(jewel)
                    current_effect.pop(j)
                    break

    def __parse_profile_card_slot__(self, bs_object: BeautifulSoup):
        profile_card_slot = bs_object.find("div", {"class": "profile-card__list"})

        print(profile_card_slot)


    def __parse__(self, bs_object: BeautifulSoup):
        # profile-equipment-character
        self.__parse_profile_equipment_character__(bs_object)

        # profile-equipment-slot
        self.__parse_profile_equipment_slot__(bs_object)

        # profile-avatar
        self.__parse_profile_avatar_slot__(bs_object)

        # profile-jewel
        self.__parse_profile_jewel_slot__(bs_object)

        # profile-card
        self.__parse_profile_card_slot__(bs_object)


    @property
    def src(self):
        return self.__src

    @property
    def equipment_slot(self):
        return self.__equipment_slot

    @property
    def avatar_slot(self):
        return self.__avatar_slot

    @property
    def jewel_slot(self):
        return self.__jewel_slot

    @property
    def card_slot(self):
        return self.__card_slot
