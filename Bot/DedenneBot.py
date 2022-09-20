from enum import Enum

import discord

from youtube.youtube import YoutubeHandler
from util import *

class DedenneBot(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)
        self.__words = parse_json("data/command_collection.json")
        self.youtube_handler = YoutubeHandler(parse_json("data/info.json")["youtube"]["api_key"])

        self.task = {}

    async def on_message(self, message):
        # '봇' 또는 'bot' 이 포함된 채널에만 반응
        if "봇" not in message.channel.name and "bot" not in message.channel.name:
            return

        # 본인이 보낸 메시지에는 반응하지 않음
        if message.author == self.user:
            return

        return_words = self.__get_return_words(message.content)

        if return_words is not None:
            words = return_words.split("_")

            command = words[0]
            content = words[1]

            # 단순 출력 커맨드
            if command == "m":
                await message.channel.send(content + " " + message.author.name)

            # 명령어
            elif command == "c":
                command_contents = self.__get_command_contents(content)

                if content == "!help":
                    await message.channel.send(command_contents["text"])

                elif content == "!search":
                    keyword = " ".join(message.content.split()[1:])

                    search_result = self.youtube_handler.get_search_result(keyword)
                    await message.channel.send(self.__get_search_result_string(search_result))

                    self.__add_task(
                        channel_id=message.channel.id,
                        user_id=message.author.id,
                        search_result=search_result
                    )

                elif content == "!select":
                    search_result = self.__get_task(
                        channel_id=message.channel.id,
                        user_id=message.author.id
                    )

                    if search_result is not None:
                        num = int(message.content.split()[1])

                        if 0 < num <= len(search_result):
                            target = search_result[num-1]

                            await message.channel.send(target["url"])

                else:
                    await message.channel.send("%s 기능 미구현" % content)

        else:
            await message.channel.send(message.content)

    def __add_task(self, channel_id, user_id, search_result):
        key = str(channel_id)+"``"+str(user_id)

        self.task[key] = search_result

    def __get_task(self, channel_id, user_id):
        key = str(channel_id)+"``"+str(user_id)

        if key in self.task.keys():
            return self.task.pop(key)
        else:
            return None


    def __get_search_result_string(self, search_result):
        msg = "[검색결과]\n"

        for i in range(len(search_result)):
            item = search_result[i]

            # url = "https://www.youtube.com/watch?v=" + item["id"]
            msg += "  " + str(i + 1) + ". " + item["title"] + "\n"

        msg += "**선택 n으로 입력>>**"
        return msg

    def __get_return_words(self, message):
        for item in self.__words["words"]:
            for word in item["trigger_words"]:
                if word in message:
                    return item["return_word"]

        return None

    def __get_command_contents(self, command):
        for item in self.__words["commands"]:
            if item["command"] == command:
                return item

        return None
