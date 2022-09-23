from lostark.data.profile_character_list import Character


class Server:
    def __init__(self, server: str):
        self.__server = server

        self.__characters = []

    def __str__(self):
        s = self.server + "\n"
        for character in self.characters:
            s += str(character) + "\n"

        return s

    # 서버
    @property
    def server(self):
        return self.__server

    # 서버에 소속된 캐릭터들
    @property
    def characters(self):
        return self.__characters

    def add_character(self, job: str, src: str, lv: str, name: str):
        self.__characters.append(Character(job, src, lv, name))
