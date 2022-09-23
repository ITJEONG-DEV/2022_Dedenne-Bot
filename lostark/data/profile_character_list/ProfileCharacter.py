from lostark.data.profile_character_list import Server
from lostark.util import *


class ProfileCharacter:
    def __init__(self, bs_object: BeautifulSoup):
        self.__servers = []
        self.__parse__(bs_object)

    def __str__(self):
        s = "보유 캐릭터\n"
        for server in self.character_list:
            s += str(server) + "\n"

        return s

    def __parse__(self, bs_object: BeautifulSoup):
        server_list = bs_object.findAll("strong")

        all_characters_list = bs_object.findAll("ul")

        for i in range(len(server_list)):
            server_name = server_list[i].text[1:].strip()

            server = Server(server_name)

            characters = get_bs_object(all_characters_list[i]).findAll("li")
            for j in range(len(characters)):
                character = get_bs_object(characters[j])
                span = character.findAll("span")[0]
                img = character.img

                name = character.findAll("span")[-1].text.strip()
                total = span.text.strip()
                lv = span.text.strip()[:len(total)-len(name)]

                server.add_character(
                    name=name,
                    job=img["alt"].strip(),
                    lv=lv,
                    src=img["src"].strip()
                )

            self.__add_server__(server)

    def __add_server__(self, server: Server):
        self.character_list.append(server)

    # 서버별 캐릭터 리스트
    @property
    def character_list(self):
        return self.__servers
