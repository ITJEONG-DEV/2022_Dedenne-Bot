import re
import json

from . import Slot, Jewel, Card, CardEffect, CardDeck
from . import ProfileAbilityEngrave
from lostark.util import *


class ProfileEquipment:
    def __init__(self, bs_object: BeautifulSoup):
        self.__src = ""

        self.__equipment_slot = []
        self.__equipment_set_effect = set([])

        self.__avatar_slot = []
        self.__jewel_slot = []
        self.__card_deck = None
        self.__ability_engrave = []

        self.__parse__(bs_object)

    def __str__(self):
        s = self.src + "\n"

        s += "\n착용 장비\n"
        for slot in self.__equipment_slot:
            s += str(slot) + "\n"

        s += "\n장비 세트 효과\n"
        for slot in self.__equipment_set_effect:
            s += str(slot) + "\n"

        s += "\n아바타\n"
        for slot in self.__avatar_slot:
            s += str(slot) + "\n"

        s += "\n보석\n"
        for slot in self.__jewel_slot:
            s += str(slot) + "\n"

        s += str(self.__card_deck)

        s += str(self.__ability_engrave)

        return s

    def __parse_profile_equipment_character__(self, bs_object: BeautifulSoup):
        profile_equipment_character = bs_object.find("div", {"class": "profile-equipment__character"})
        img = get_bs_object(profile_equipment_character).img
        self.__src = img["src"]

    def __parse_profile_equipment_slot__(self, bs_object: BeautifulSoup, script: json):
        if script is None:
            return

        profile_equipment_slot = bs_object.find("div", {"class": "profile-equipment__slot"})
        equipment_slot = get_bs_object(profile_equipment_slot).findAll("div")

        for i in range(len(equipment_slot)):
            slot = get_bs_object(equipment_slot[i]).div
            class_name = slot["class"][0]

            if "profile" in class_name:
                continue

            try:
                item_data = slot["data-item"]
                grade = slot["data-grade"]

                img = get_bs_object(slot).img
                src = img["src"]

                slot = Slot(
                    class_name=class_name,
                    grade=grade,
                    item=item_data,
                    src=src
                )

                self.__equipment_slot.append(slot)

                data = script["Equip"][item_data]

                # set name
                top_str = data["Element_009"]["value"]["Element_000"]["topStr"]
                set_name = get_bs_object(top_str).find("font").text

                # set effect
                set_effect_obj = data["Element_009"]["value"]
                for item in set_effect_obj.items():
                    content = item[1]["topStr"]
                    name = " ".join(get_bs_object(content).find("font").text.split("[")[0].split(" ")[:-1])
                    lv = get_bs_object(content).find("font", {"color": "#FFD200"})
                    if lv is not None:
                        lv = lv.text
                        effect = get_bs_object(item[1]["contentStr"]["Element_000"]["contentStr"]).find("font").text

                        self.__equipment_set_effect.add(f"{set_name}\t{name}\t{lv}\t{effect}")

                    # print(item)

            except Exception as e:
                print("Error: " + str(e))

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

            try:
                item_data = slot["profile-item"]

                img = get_bs_object(slot).img
                src = img["src"]

                self.__avatar_slot.append(Slot(
                    class_name=class_name,
                    grade=grade,
                    item=item_data,
                    src=src
                ))
            except KeyError:
                continue

    def __parse_profile_jewel_slot__(self, bs_object: BeautifulSoup, script: json):
        if script is None:
            return

        profile_jewel_slot = bs_object.find("div", {"class": "jewel-effect__wrap"})

        jewel_wrap = get_bs_object(profile_jewel_slot).find("div", {"class": "jewel__wrap"})
        jewel_span_list = get_bs_object(jewel_wrap).findAll("span")

        jewel_effect = get_bs_object(profile_jewel_slot).find("div", {"class": "box_wrapper"})
        jewel_effect_list = get_bs_object(jewel_effect).findAll("li")

        # current jewel
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

        # current effect
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

        # jewel name
        items = {}
        for item in script["Equip"].items():
            if "Gem" in item[0]:
                text = get_bs_object(item[1]["Element_000"]["value"]).find("p").text
                items[item[0]] = text

        for i in range(len(current_jewel)):
            for j in range(len(current_effect)):
                if current_jewel[i]["id"] == current_effect[j]["id"]:
                    jewel = Jewel(
                        jewel_id=current_jewel[i]["id"],

                        name=items[current_jewel[i]["item_data"]],

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
        self.__card_deck = CardDeck()

        # card
        profile_card_slot = bs_object.find("div", {"class": "profile-card__list"})
        card_list = get_bs_object(profile_card_slot).findAll("li")
        for i in range(len(card_list)):
            card_item = get_bs_object(card_list[i])

            index = card_item.li["data-cardindex"]

            slot = get_bs_object(card_item.find("div", {"class": "card-slot"}))

            grade = slot.div["data-grade"]
            item_data = slot.div["data-item"]

            name = get_bs_object(slot.div).find("font").text

            img = get_bs_object(slot.div).find("img")
            src = get_bs_object(img).img["src"]

            card = Card(
                name=name,
                index=index,
                grade=grade,
                item_data=item_data,
                src=src
            )

            self.__card_deck.add_card(card)

        # effect
        profile_card_text = bs_object.find("div", {"class": "profile-card__content"})
        effect_list = get_bs_object(profile_card_text).findAll("li")
        for i in range(len(effect_list)):
            effect_item = get_bs_object(effect_list[i]).li

            index = effect_item["data-cardsetindex"]

            title = get_bs_object(effect_item).find("div", {"class": "card-effect__title"}).text
            description = get_bs_object(effect_item).find("div", {"class": "card-effect__dsc"}).text

            effect = CardEffect(
                index=index,
                title=title,
                description=description
            )

            self.__card_deck.add_effect(effect)

    def __parse_profile_ability_engrave__(self, bs_object: BeautifulSoup):
        self.__ability_engrave = ProfileAbilityEngrave()

        # card
        profile_ability_engrave = bs_object.find("div", {"class": "profile-ability-engrave"})
        ability_ul = get_bs_object(profile_ability_engrave).findAll("ul")

        for ul in ability_ul:
            ability_li = get_bs_object(ul).findAll("li")
            for li in ability_li:
                ability = get_bs_object(li).find("span").text
                effect = get_bs_object(li).find("p").text

                self.__ability_engrave.add_ability(ability, effect)

    def __parse__(self, bs_object: BeautifulSoup):
        scripts = bs_object.findAll("script")
        target_script = None
        for script in scripts:
            if "Profile = {" in script.text:
                matched = re.search(r'Profile = (.*?);', script.text, re.S)
                target_script = json.loads(matched.group(1))

        # profile-equipment-character
        self.__parse_profile_equipment_character__(bs_object)

        # profile-equipment-slot
        self.__parse_profile_equipment_slot__(bs_object, target_script)

        # profile-avatar
        self.__parse_profile_avatar_slot__(bs_object)

        # profile-jewel
        self.__parse_profile_jewel_slot__(bs_object, target_script)

        # profile-card
        self.__parse_profile_card_slot__(bs_object)

        # profile-ability-engrave
        self.__parse_profile_ability_engrave__(bs_object)

    @property
    def src(self):
        return self.__src

    @property
    def equipment_slot(self):
        return self.__equipment_slot

    @property
    def equipment_effect_slot(self):
        return self.__equipment_set_effect

    @property
    def avatar_slot(self):
        return self.__avatar_slot

    @property
    def jewel_slot(self):
        return self.__jewel_slot

    @property
    def card_slot(self):
        return self.__card_deck

    @property
    def ability_engrave_slot(self):
        return self.__ability_engrave
