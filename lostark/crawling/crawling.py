import urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup

from lostark.data.Profile import Profile


def get_html_object(url="https://lostark.game.onstove.com/Profile/Character/허니퓨"):
    html = urlopen(url)
    return BeautifulSoup(html, "html.parser")


def get_html_object_korean(default_url="https://lostark.game.onstove.com/Profile/Character/", character_name="허니퓨"):
    character_name = urllib.parse.quote_plus(character_name)
    url = default_url + character_name

    return get_html_object(url)


def get_character_data(base_url="https://lostark.game.onstove.com/Profile/Character/", character_name="wpqlRhc"):
    character_name = urllib.parse.quote_plus(character_name)
    bs_object = get_html_object(base_url + character_name)

    return Profile(bs_object)


if __name__ == "__main__":
    bs_object = get_html_object_korean()
    print(str(bs_object))

    # data = get_character_data(character_name="데덴네귀여워")

    # print(str(data))
