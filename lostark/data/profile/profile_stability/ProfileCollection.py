from lostark.util import *


class ProfileCollection:
    def __init__(self, bs_object: BeautifulSoup):
        # heart
        div = bs_object.find("div", {"class": "lui-tab__content heart"})
        field = get_bs_object(div).find("div", {"class": "collection-status"})
        p = get_bs_object(field).find("p").text
        self.__heart = p

        # island
        div = bs_object.find("div", {"class": "lui-tab__content island"})
        field = get_bs_object(div).find("div", {"class": "collection-status"})
        p = get_bs_object(field).find("p").text
        self.__island = p

        # seed
        div = bs_object.find("div", {"class": "lui-tab__content seed"})
        field = get_bs_object(div).find("div", {"class": "collection-status"})
        p = get_bs_object(field).find("p").text
        self.__seed = p

        # art
        div = bs_object.find("div", {"class": "lui-tab__content art"})
        field = get_bs_object(div).find("div", {"class": "collection-status"})
        p = get_bs_object(field).find("p").text
        self.__art = p

        # voyage
        div = bs_object.find("div", {"class": "lui-tab__content voyage"})
        field = get_bs_object(div).find("div", {"class": "collection-status"})
        p = get_bs_object(field).find("p").text
        self.__voyage = p

        # tree
        div = bs_object.find("div", {"class": "lui-tab__content tree"})
        field = get_bs_object(div).find("div", {"class": "collection-status"})
        p = get_bs_object(field).find("p").text
        self.__tree = p

        # medal
        div = bs_object.find("div", {"class": "lui-tab__content medal"})
        field = get_bs_object(div).find("div", {"class": "collection-status"})
        p = get_bs_object(field).find("p").text
        self.__medal = p

        # star
        div = bs_object.find("div", {"class": "lui-tab__content star"})
        field = get_bs_object(div).find("div", {"class": "collection-status"})
        p = get_bs_object(field).find("p").text
        self.__star = p

        # memory
        div = bs_object.find("div", {"class": "lui-tab__content memory"})
        field = get_bs_object(div).find("div", {"class": "collection-status"})
        p = get_bs_object(field).find("p").text
        self.__memory = p

    def __str__(self):
        return f"거인의심장: {self.heart}\n" + f"섬의 마음: {self.island}\n" + f"모코코 씨앗: {self.seed}\n" \
               + f"위대한 미술품: {self.art}\n" + f"항해 모험물: {self.voyage}\n" + f"세계수의 잎: {self.tree}\n" \
               + f"이그네아의 징표: {self.medal}\n" + f"오르페우스의 별: {self.star}\n" + f"기억의 오르골: {self.memory}\n"

    @property
    def heart(self):
        return self.__heart

    @property
    def island(self):
        return self.__island

    @property
    def seed(self):
        return self.__seed

    @property
    def art(self):
        return self.__art

    @property
    def voyage(self):
        return self.__voyage

    @property
    def tree(self):
        return self.__tree

    @property
    def medal(self):
        return self.__medal

    @property
    def star(self):
        return self.__star

    @property
    def memory(self):
        return self.__memory
