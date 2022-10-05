import datetime
import re

from lostark.util import *


class Engraved:
    def __init__(self, name, price):
        self.__name = name
        self.__price = price

    def __str__(self):
        return f"{self.name} {self.price} 골드"

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price


class GoldInfo:
    def __init__(self, bs_object: BeautifulSoup, base_url: str):
        self.__url = base_url

        self.__engraveds = []
        self.__golds = {}

        self.__time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        scripts = bs_object.findAll("script")
        for script in scripts:
            if "window.__NUXT__" in script.text:
                matched = re.search(r'window.__NUXT__=(.*?);', script.text, re.S)
                splits = matched.group(1).split("(")
                contents = splits[2].split(")")[1]
                param = splits[-1].split(")")[0]

                matched = re.search(r'{engraveds:(.*?)]}', contents, re.S)
                engraveds = matched.group(1)

                matched = re.search(r'lospi:(.*?)},', contents, re.S)
                golds = matched.group(1)

                self.__parse(engraveds, param, golds)

                break

    def __str__(self):
        s = str(self.__golds) + "\n"

        for item in self.engraveds:
            s += str(item) + "\n"

        return s

    def __parse(self, engraveds, param, golds):
        # engraveds
        items = engraveds.split("{")
        for item in items:
            if "id" not in item:
                continue

            matched = re.search(r'name:(.*?),', item, re.S)
            name = matched.group(1)[1:-1]

            matched = re.search(r'lowestPrice:(.*?),', item, re.S)
            low_price = matched.group(1)

            try:
                low_price = int(low_price)
            except:
                low_price = int(self.__matched_parm(low_price, param))

            self.__engraveds.append(Engraved(name, low_price))

        # golds
        matched = re.search(r'sell:(.*?),', golds, re.S)
        sell = matched.group(1)

        buy = golds.split(":")[-1]

        self.__golds["sell"] = sell
        self.__golds["buy"] = buy

    def __matched_parm(self, content: str, param: str):
        params = param.split(",")

        index = ord(content) - ord('a')

        return params[index]

    @property
    def time(self):
        return self.__time

    @property
    def url(self):
        return self.__url

    @property
    def engraveds(self):
        return self.__engraveds

    @property
    def golds(self):
        return self.__golds
