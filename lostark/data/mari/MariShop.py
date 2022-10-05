from lostark.util import *


class MariShop:
    def __init__(self, bs_object: BeautifulSoup, base_url: str):
        self.__url = base_url

        self.__title = ""

        self.__tab1_name = ""
        self.__tab2_name = ""

        self.__tab1 = []
        self.__tab2 = []

        self.__tab1_pre = []
        self.__tab2_pre = []

        self.__parse(bs_object)

    def __str__(self):
        s = f"{self.tab1_name}\n"
        s += "현재 판매 상품\n"
        for i in range(len(self.tab1)):
            item = self.tab1[i]
            s += f"  {i + 1}. {item[0]} 크리스탈 {item[1]}\n"

        s += "이전 판매 상품\n"
        if len(self.tab1_pre) > 0:
            for i in range(len(self.tab1_pre)):
                item = self.tab1_pre[i]
                s += f"  {i + 1}. {item[0]} 크리스탈 {item[1]}\n"
        else:
            s += "  이전 판매 상품이 없습니다\n"

        s += f"\n{self.tab2_name}\n"
        for i in range(len(self.tab2)):
            item = self.tab2[i]
            s += f"  {i + 1}. {item[0]} 크리스탈 {item[1]}\n"

        s += "이전 판매 상품\n"
        if len(self.tab2_pre) > 0:
            for i in range(len(self.tab2_pre)):
                item = self.tab2_pre[i]
                s += f"  {i + 1}. {item[0]} 크리스탈 {item[1]}\n"
        else:
            s += "  이전 판매 상품이 없습니다\n"

        return s

    def __parse(self, bs_object: BeautifulSoup):
        mari = bs_object.find("div", {"class": "shop-tab"})
        self.__title = get_bs_object(mari).find("a", {"href": "#mari"}).text

        lui_tab_menu = bs_object.find("div", {"class": "lui-tab__menu"})

        self.__tab1_name = get_bs_object(lui_tab_menu).find("a", {"href": "#lui-tab1-1"}).text
        self.__tab2_name = get_bs_object(lui_tab_menu).find("a", {"href": "#lui-tab1-2"}).text

        # tab1
        lui_tab1_1 = bs_object.find("div", {"id": "lui-tab1-1"})

        # current
        current = get_bs_object(lui_tab1_1).find("ul", "list-items")
        item_list = get_bs_object(current).findAll("div", {"class": "wrapper"})

        for item in item_list:
            item_object = get_bs_object(item)
            item_name = item_object.find("span", {"class": "item-name"}).text
            amount = item_object.find("span", {"class": "amount"}).text

            self.__tab1.append([item_name, amount])

        # pre
        pre_text = get_bs_object(lui_tab1_1).find("p", {"class": "is-active"})
        pre = get_bs_object(lui_tab1_1).find("div", "swiper-container")
        if pre is not None:
            item_list = get_bs_object(pre).findAll("div", {"class": "wrapper"})

            for item in item_list:
                item_object = get_bs_object(item)
                item_name = item_object.find("span", {"class": "item-name"}).text
                amount = item_object.find("span", {"class": "amount"}).text

                self.__tab1_pre.append([item_name, amount])

        # tab2
        lui_tab1_2 = bs_object.find("div", {"id": "lui-tab1-2"})

        # current
        current = get_bs_object(lui_tab1_2).find("ul", "list-items")
        item_list = get_bs_object(current).findAll("div", {"class": "wrapper"})

        for item in item_list:
            item_object = get_bs_object(item)
            item_name = item_object.find("span", {"class": "item-name"}).text
            amount = item_object.find("span", {"class": "amount"}).text

            self.__tab2.append([item_name, amount])

        # pre
        pre_text = get_bs_object(lui_tab1_2).find("p", {"class": "is-active"})
        pre = get_bs_object(lui_tab1_2).find("div", "swiper-container")
        if pre is not None:
            item_list = get_bs_object(pre).findAll("div", {"class": "wrapper"})

            for item in item_list:
                item_object = get_bs_object(item)
                item_name = item_object.find("span", {"class": "item-name"}).text
                amount = item_object.find("span", {"class": "amount"}).text

                self.__tab2_pre.append([item_name, amount])

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    @property
    def tab1_name(self):
        return self.__tab1_name

    @property
    def tab2_name(self):
        return self.__tab2_name

    @property
    def tab1(self):
        return self.__tab1

    @property
    def tab1_pre(self):
        return self.__tab1_pre

    @property
    def tab2(self):
        return self.__tab2

    @property
    def tab2_pre(self):
        return self.__tab2_pre
