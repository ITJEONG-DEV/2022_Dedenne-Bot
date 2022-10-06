import datetime

from bot.botWorker import *
from data import *
from util import parse_json

from lostark import get_character_data, get_mari_shop, get_gold_info
from bot.view import *

import discord

KOREA = datetime.timezone(datetime.timedelta(hours=9))

class DedenneBot(discord.Client):
    async def on_ready(self):
        # word profile
        self.__words = parse_json("json/command_collection.json")
        self.__error_messages = parse_json("json/error_messages.json")

        # bot worker
        self.__worker = BotWorker(self)

        print('Logged on as', self.user)

    async def on_message(self, message):
        await self.wait_until_ready()

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
                    await self.search_lostark(message)

                elif content == "mari":
                    await self.show_mari_shop(message)

                elif content == "gold":
                    await self.show_gold_info(message)

    async def search_lostark(self, message):
        keyword = message.content.split()[-1]
        data = get_character_data(character_name=keyword)

        if data is None:
            await self.send_specify_message(channel=message.channel, error_name="character_not_found", name=keyword)

        else:

            embed = discord.Embed(
                title=data.name + "@" + data.server + " " + data.lv,
                url="https://lostark.game.onstove.com/Profile/Character/" + data.name,
                color=discord.Color.blue()
            )

            embed.set_image(url=data.profile_ingame.profile_equipment.src)
            embed.set_footer(text=data.name + "\t\t\t" + data.time + " 기준", icon_url=data.emblem)

            embed.add_field(name="원정대 레벨", value=f"`{data.profile_ingame.profile_info.expedition_lv}`")
            embed.add_field(name="아이템 레벨", value=f"`{data.profile_ingame.profile_info.equip_item_lv}`")
            embed.add_field(name="영지",
                            value=f"`{data.profile_ingame.profile_info.estate_name} {data.profile_ingame.profile_info.estate_lv}`")

            m = "```diff\n"
            for slot in data.profile_ingame.profile_equipment.ability_engrave_slot.ability:
                if "감소" in str(slot):
                    m += "-" + str(slot) + "\n"
                else:
                    m += "+" + str(slot) + "\n"
            if m == "```diff\n":
                m = "-"
            else:
                m += "```"
            embed.add_field(name="각인 효과", value=m)

            m = f" 공격력 `{data.state.attack}`\n최대 생명력 `{data.state.hp}`"
            embed.add_field(name="기본 특성", value=m)

            options = CharacterView(data=data)

            message = await message.channel.send(embed=embed, view=options)
            options.set_message(message)

    async def show_mari_shop(self, message):
        data = get_mari_shop()

        embed = discord.Embed(
            title=data.title,
            url=data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=data.time + " 기준")

        m = ""
        for i in range(len(data.tab1)):
            item = data.tab1[i]
            m += f"```diff\n+{item[0]}\n-크리스탈 {item[1]}\n```"
        if m == "":
            m = "현재 판매 상품이 없습니다"
        embed.add_field(name="현재 판매 상품", value=m)

        pre_num = int(len(data.tab1_pre) / 6)

        for i in range(pre_num):
            m = ""
            for j in range(6):
                item = data.tab1_pre[i * 6 + j]
                m += f"```diff\n+{item[0]}\n-크리스탈 {item[1]}\n```"
            if m == "":
                m = "이전 판매 상품이 없습니다"
            embed.add_field(name=data.tab1_pre_name[i], value=m)

        options = MariShopView(data=data)

        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_gold_info(self, message):
        data = get_gold_info()

        embed = discord.Embed(
            title="골드 시세",
            url=data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=data.time + " 기준")

        embed.add_field(name="💎골드 팔 때", value=f"```yaml\n{data.golds['sell']}\n```")
        embed.add_field(name="💰골드 살 때", value=f"```fix\n{data.golds['buy']}\n```")

        options = GoldView(data=data)

        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

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
