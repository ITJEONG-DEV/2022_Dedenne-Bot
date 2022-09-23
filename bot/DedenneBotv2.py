from bot.botWorker import *
from data import *
from util import parse_json

from lostark import get_character_data

import discord

ready = False


class DedenneBot(discord.Client):
    async def on_ready(self):
        # word data
        self.__words = parse_json("json/command_collection.json")
        self.__error_messages = parse_json("json/error_messages.json")

        # bot worker
        self.__worker = BotWorker(self)

        global ready
        ready = True

        print('Logged on as', self.user)

    async def on_message(self, message):
        global ready
        if not ready:
            return

        # '봇' 또는 'bot' 이 포함된 채널에만 반응
        if "봇" not in message.channel.name and "bot" not in message.channel.name:
            return

        if message.author == self.user:
            return

        return_words = self.__get_return_words(message.content)

        if return_words is not None:
            words = return_words.split("_")

            command = words[0]
            content = words[1]

            if command == "m":
                await self.send_message(message.channel, content + " " + message.author.name)

            elif command == "c":
                item = Work(
                    command=content,
                    contents={
                        "guild": message.guild,
                        "channel": message.channel,
                        "author": message.author,
                        "message": message.content
                    }
                )

                await self.__worker.handle(item)

            elif command == "l":
                if content == "search":
                    keyword = message.content.split()[-1]
                    data = get_character_data(character_name=keyword)

                    message1 = "{} {} {}\n".format(data.server, data.name, data.lv)
                    message2 = "원정대 {}, 전투 {}\n장착 아이템 {}, 달성 아이템 {}\n칭호 {}, 길드 {}, PVP {}, 영지 {}, {}\n" \
                        .format(data.profile_ingame.profile_info.expedition_lv,
                                data.profile_ingame.profile_info.battle_lv,
                                data.profile_ingame.profile_info.equip_item_lv,
                                data.profile_ingame.profile_info.achieve_item_lv,
                                data.profile_ingame.profile_info.title,
                                data.profile_ingame.profile_info.guild,
                                data.profile_ingame.profile_info.pvp_lv,
                                data.profile_ingame.profile_info.estate_name,
                                data.profile_ingame.profile_info.estate_lv)

                    await self.send_message(message.channel, message1 + message2)
                    await self.send_message(message.channel, data.profile_ingame.profile_equipment.src)

    async def send_specify_message(self, channel, error_name: str, name: str = ""):
        words = self.__error_messages[error_name]

        message = ""
        for word in words:
            if word.startswith('!'):
                message += name
            else:
                message += word

            message += " "

        await self.send_message(channel, message)

    async def send_message(self, channel, contents):
        await channel.send(contents)

    def __get_return_words(self, message):
        for item in self.__words["words"]:
            for word in item["trigger_words"]:
                if word in message:
                    return item["return_word"]

        return None
