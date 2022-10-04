from bot.botWorker import *
from data import *
from util import parse_json

from lostark import get_character_data
from lostark import Profile

import discord

ready = False

import unicodedata


def fill_str_with_space(input_s="", max_size=40, fill_char="*"):
    """
    - 길이가 긴 문자는 2칸으로 체크하고, 짧으면 1칸으로 체크함.
    - 최대 길이(max_size)는 40이며, input_s의 실제 길이가 이보다 짧으면
    남은 문자를 fill_char로 채운다.
    """
    l = 0
    for c in input_s:
        if unicodedata.east_asian_width(c) in ['F', 'W']:
            l += 2
        else:
            l += 1
    return input_s + fill_char * (max_size - l)


class Options(discord.ui.View):
    def __init__(self, data: Profile):
        super().__init__()

        self.message = None
        self.data = data

    def set_message(self, message):
        self.message = message

    @discord.ui.button(label="기본 정보", style=discord.ButtonStyle.grey)
    async def on_click_default_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data.name + "@" + self.data.server + " " + self.data.lv,
            url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
            color=discord.Color.blue()
        )

        embed.set_image(url=self.data.profile_ingame.profile_equipment.src)
        embed.set_footer(text=self.data.name, icon_url=self.data.emblem)

        embed.add_field(name="원정대 레벨", value=self.data.profile_ingame.profile_info.expedition_lv)
        embed.add_field(name="아이템 레벨", value=self.data.profile_ingame.profile_info.equip_item_lv)
        embed.add_field(name="영지",
                        value=f"**{self.data.profile_ingame.profile_info.estate_name}  {self.data.profile_ingame.profile_info.estate_lv}**")

        m = ""
        for slot in self.data.profile_ingame.profile_equipment.ability_engrave_slot.ability:
            m += str(slot) + "\n"
        embed.add_field(name="각인 효과", value=m)

        m = f"공격력 {self.data.state.attack}\n최대 생명력 {self.data.state.hp}"
        embed.add_field(name="기본 특성", value=m)

        # default_info = [
        #     f"**{self.data.lv}**",
        #     f"원정대 레벨 **{self.data.profile_ingame.profile_info.expedition_lv}**\n 아이템 레벨 **{self.data.profile_ingame.profile_info.equip_item_lv}**/**{self.data.profile_ingame.profile_info.achieve_item_lv}**",
        #     f"칭호 **{self.data.profile_ingame.profile_info.title}**\n길드 **{self.data.profile_ingame.profile_info.guild}**  PVP **{self.data.profile_ingame.profile_info.pvp_lv}**",
        #     f"영지  **{self.data.profile_ingame.profile_info.estate_name}  {self.data.profile_ingame.profile_info.estate_lv}**"
        # ]
        #
        # embed.add_field(name=self.data.name+"@"+self.data.server+" "+self.data.lv, value="\n".join(default_info))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="세트효과 정보", style=discord.ButtonStyle.grey)
    async def on_click_set_effect(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data.name + "@" + self.data.server + " " + self.data.lv,
            url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.name, icon_url=self.data.emblem)

        # m = ""
        # for card in self.data.profile_ingame.profile_equipment.card_slot.cards:
        #     m += f"{card.name}\n"
        #
        # embed.add_field(name="카드 정보", value=m)

        m = ""
        for effect in self.data.profile_ingame.profile_equipment.card_slot.effect:
            m += f"{effect.title}\n"
        embed.add_field(name="카드 세트 효과", value=m)

        m = ""
        for effect in self.data.profile_ingame.profile_equipment.equipment_effect_slot:
            m += " ".join(effect.split("\t")[:-1]) + "\n"
        embed.add_field(name="장비 세트 효과", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="특성 정보", style=discord.ButtonStyle.grey)
    async def on_click_ability_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data.name + "@" + self.data.server + " " + self.data.lv,
            url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
            color=discord.Color.blue()
        )

        # embed.set_image(url=self.data.profile_ingame.profile_equipment.src)
        embed.set_thumbnail(url=self.data.profile_ingame.profile_equipment.src)
        embed.set_footer(text=self.data.name, icon_url=self.data.emblem)

        m = f"치명 {self.data.state.fatal}\n특화 {self.data.state.specialization}\n제압 {self.data.state.overpowering}\n신속 {self.data.state.swiftness}\n인내 {self.data.state.patience}\n숙련 {self.data.state.skilled}"
        embed.add_field(name="전투 특성", value=m)

        state = self.data.profile_state
        m = f"지성 {state.intellect}\n담력 {state.courage}\n매력 {state.charm}\n친절 {state.kindness}\n"
        embed.add_field(name="성향", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="보유 캐릭터", style=discord.ButtonStyle.grey)
    async def on_click_character_list(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data.name + "@" + self.data.server + " " + self.data.lv,
            url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url=self.data.profile_ingame.profile_equipment.src)

        character_list = self.data.profile_character_list.character_list
        msg = "\n"
        for server in character_list:
            msg += "**" + server.server + "**\n"
            for character in server.characters:
                msg += character.name + " " + character.lv + " " + character.job + "\n"
            msg += "\n"

        embed.add_field(name="보유 캐릭터 목록", value=msg)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="보석 정보", style=discord.ButtonStyle.grey)
    async def on_click_jewel(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data.name + "@" + self.data.server + " " + self.data.lv,
            url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.name, icon_url=self.data.emblem)

        m = ""
        for jewel in self.data.profile_ingame.profile_equipment.jewel_slot:
            m += f"{jewel.name} {jewel.skill_name} {jewel.effect}\n"

        embed.add_field(name="보석 정보", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()


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
                    await self.search_lostark(message)

    async def search_lostark(self, message):
        keyword = message.content.split()[-1]
        data = get_character_data(character_name=keyword)

        embed = discord.Embed(
            title=data.name + "@" + data.server + " " + data.lv,
            url="https://lostark.game.onstove.com/Profile/Character/" + data.name,
            color=discord.Color.blue()
        )

        embed.set_image(url=data.profile_ingame.profile_equipment.src)
        embed.set_footer(text=data.name, icon_url=data.emblem)

        embed.add_field(name="원정대 레벨", value=data.profile_ingame.profile_info.expedition_lv)
        embed.add_field(name="아이템 레벨", value=data.profile_ingame.profile_info.equip_item_lv)
        embed.add_field(name="영지",
                        value=f"**{data.profile_ingame.profile_info.estate_name}  {data.profile_ingame.profile_info.estate_lv}**")

        m = ""
        for slot in data.profile_ingame.profile_equipment.ability_engrave_slot.ability:
            m += str(slot) + "\n"
        embed.add_field(name="각인 효과", value=m)

        m = f"공격력 {data.state.attack}\n최대 생명력 {data.state.hp}"
        embed.add_field(name="기본 특성", value=m)

        # default_info = [
        #     f"원정대 레벨 **{data.profile_ingame.profile_info.expedition_lv}**\n 아이템 레벨 **{data.profile_ingame.profile_info.equip_item_lv}**/**{data.profile_ingame.profile_info.achieve_item_lv}**",
        #     f"칭호 **{data.profile_ingame.profile_info.title}**\n길드 **{data.profile_ingame.profile_info.guild}**  PVP **{data.profile_ingame.profile_info.pvp_lv}**",
        #     f"영지  **{data.profile_ingame.profile_info.estate_name}  {data.profile_ingame.profile_info.estate_lv}**"
        # ]
        #
        # embed.add_field(name=data.name+"@"+data.server+" "+data.lv, value="\n".join(default_info))

        options = Options(data=data)

        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)
        # await self.send_message(message.channel, message1 + message2)
        # await self.send_message(message.channel, data.profile_ingame.profile_equipment.src)

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
