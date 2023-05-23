import datetime
import json
import os

import imageio as imageio

from util import parse_json

from lostark import get_character_data, get_mari_shop, get_engraving_item, get_news, get_markets, get_adventure_island, \
    get_challenge_abyss_dungeons, get_challenge_guardian_raids, get_callendar, get_gems, parse_adventure_island, \
    get_character_info
from bot.view import *

import random

from . import DBManager

import discord

KOREA = datetime.timezone(datetime.timedelta(hours=9))
file_dir = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\lostark\\adventure_island\\date.txt"

ready = False

on_ads = False


async def send_message(channel, message=None, file=None, embeds=None, embed=None, view=None, ads=False):
    if ads:
        embeds = []
        files = []
        for i in range(0, 2):
            if i == 0:
                embed = discord.Embed(
                    title=f"모코콩 4종",
                    color=discord.Color.blue()
                )
                file = discord.File(f'ads/{1}.jpg')
                embed.set_image(url=f'attachment://{1}.jpg')
                embed.set_footer(text="찍은사람: 허니퓨")

            elif i == 1:
                embed = discord.Embed(
                    title=f"잘생긴 헌터즈",
                    color=discord.Color.blue()
                )
                file = discord.File(f'ads/{2}.jpg')
                embed.set_image(url=f'attachment://{2}.jpg')
                embed.set_footer(text="찍은사람: 데.귀")

            embeds.append(embed)
            files.append(file)

        await channel.send(files=files, embeds=embeds)

    else:
        _ = await channel.send(content=message, file=file, embeds=embeds, embed=embed, view=view)

        if on_ads:
            index = random.randint(1, 2)

            if index == 1:
                embed = discord.Embed(
                    title=f"모코콩 4종",
                    color=discord.Color.blue()
                )
                file = discord.File(f'ads/{index}.jpg')
                embed.set_image(url=f'attachment://{index}.jpg')
                embed.set_footer(text="찍은사람: 허니퓨")
                await channel.send(file=file, embed=embed)
            else:
                embed = discord.Embed(
                    title=f"잘생긴 헌터즈",
                    color=discord.Color.blue()
                )
                file = discord.File(f'ads/{index}.jpg')
                embed.set_image(url=f'attachment://{index}.jpg')
                embed.set_footer(text="찍은사람: 데.귀")
                await channel.send(file=file, embed=embed)

        return _


class DedenneBot(discord.Client):
    async def on_ready(self):
        # word profile
        self.__words = parse_json("json/command_collection.json")
        self.__error_messages = parse_json("json/error_messages.json")

        # db manager
        self.__db = DBManager()
        self.__db.connect()

        self.info = parse_json("./json/info.json")

        self.icon_url = "https://cdn-lostark.game.onstove.com/2018/obt/assets/images/common/icon/favicon-192.png"

        global ready
        ready = True

        # 957221859953352725 여기가 어디죠?
        # 1021645719528022077 디스코드봇 테스트용 서버
        for guild in self.guilds:
            if guild.id == 957221859953352725:
                for channel in guild.text_channels:
                    if "봇" in channel.name or "bot" in channel.name:
                        self.channel = channel
                        # await channel.send("데덴네봇 영업 시작!")

        print('Logged on as', self.user)

    async def on_message(self, message):
        await self.wait_until_ready()

        global ready
        if not ready:
            return

        # '봇' 또는 'bot' 이 포함된 채널에만 반응
        if message.guild.id == 957221859953352725:
            if "봇" not in message.channel.name and "bot" not in message.channel.name:
                return
        else:
            if "데덴네" not in message.channel.name:
                return

        if message.author == self.user:
            return

        return_words = self.__get_return_words(message.content)

        if return_words is not None:
            words = return_words.split("_")

            command = words[0]
            content = words[1]

            if command == "m":
                await send_message(message.channel, content)

            elif command == "l":
                # 도움말
                if content == "help":
                    await self.send_help_message(message)

                # 캐릭터 정보 조회
                elif content == "search":
                    await self.search_lostark(message)

                # 아이템 시세 조회
                elif content == "item":
                    await self.search_item(message)

                # 보석 시세 조회
                elif content == "gem":
                    await self.search_gem(message)

                # 마리샵 정보 조회
                elif content == "mari":
                    await self.show_mari_shop(message)

                # 각인서 시세 조회
                elif content == "search-engraved":
                    await self.show_search_engraved_info(message)

                # 점령전 정보
                elif content == "occupation-war":
                    await self.show_occupation_war_info(message)

                # 모험섬 정보 (수정 필요)
                elif content == "adventure-island":
                    await self.show_adventure_island_info(message)

                # 로아 소식
                elif content == "news":
                    await self.show_news(message)

                # gif
                elif content == "gif":
                    await self.make_gif(message)

                # 도비스
                elif content == "challenge-abyss-dungeons":
                    await self.show_challenge_abyss_dungeons(message)

                # 도가토
                elif content == "challenge-guardian-raids":
                    await self.show_challenge_guardian_raids(message)

                elif content == "ads":
                    await send_message(message.channel, ads=True)

    async def send_help_message(self, message):
        with open("./json/help.txt", "r", encoding='utf-8') as txt:
            content = txt.read()

            await send_message(channel=message.channel, message=content)

    async def make_gif(self, message):
        if len(message.attachments) > 0:
            # parsed option
            option = message.content.split()

            duration = 0.3

            if len(option) > 1:
                for i in range(1, len(option)):
                    word = option[i]

                    if "duration" in word:
                        duration = float(word.split("=")[1])

            dir_name = f'{message.author.id}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}'

            os.makedirs(f'result/{dir_name}', exist_ok=True)

            images = []
            for attachment in message.attachments:
                filename = f'result/{dir_name}/' + attachment.filename
                await attachment.save(filename)

                images.append(imageio.imread(filename))

            imageio.mimsave(f'result/{dir_name}/result.gif', images, duration=duration)

            await send_message(message.channel, file=discord.File(f'result/{dir_name}/result.gif'))

    async def show_challenge_abyss_dungeons(self, message):
        response = get_challenge_abyss_dungeons()

        embeds = []
        for item in response:
            embed = discord.Embed(
                title=f"{item['AreaName']} - {item['Name']}",
                color=discord.Color.blue()
            )

            embed.set_footer(icon_url=icon_url)

            # embed.add_field(name="설명", value=item['Description'])
            # embed.add_field(name="입장 가능 최소 레벨", value=f"{item['MinCharacterLevel']}/{item['MinItemLevel']}")
            embed.add_field(name="기간", value=f"{item['StartTime']} ~ {item['EndTime']}")

            embed.set_image(url=item['Image'])

            embeds.append(embed)

        if len(embeds) > 0:
            await send_message(message.channel, embeds=embeds)
        else:
            await send_message(message.channel, message="정보를 조회할 수 없습니다.")

    async def show_challenge_guardian_raids(self, message):
        response = get_challenge_guardian_raids()

        embeds = []
        for item in response["Raids"]:
            embed = discord.Embed(
                title=f"{item['Name']}",
                color=discord.Color.blue()
            )

            embed.set_footer(icon_url=icon_url)

            # embed.add_field(name="설명", value=item['Description'])
            # embed.add_field(name="입장 가능 최소 레벨", value=f"{item['MinCharacterLevel']}/{item['MinItemLevel']}")
            embed.add_field(name="기간", value=f"{item['StartTime']} ~ {item['EndTime']}")

            embed.set_image(url=item['Image'])

            embeds.append(embed)

        if len(embeds) > 0:
            await send_message(message.channel, embeds=embeds)
        else:
            await send_message(message.channel, message="정보를 조회할 수 없습니다.")

    async def show_calendar(self, message):
        data = get_callendar()

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

            message = await send_message(message.channel, embed=embed, view=options)
            options.set_message(message)

    def __get_contents(self, text):
        words = []
        for word in text.split(">"):
            if "<" in word:
                ss = word.split("<")
                words.append(ss[0])
                words.append(ss[1])
            else:
                words.append(word)

        return " ".join(filter(
            lambda k: "\n" != k and "&" not in k and "BR" not in k.upper() and "FONT" not in k.upper() and k != "",
            words)) + "\n"

    async def search_gem(self, message):
        # 보석 7
        # 보석 7홍
        # 보석 7 바드
        words = message.content.split()

        item_name = ""
        class_name = ""

        if len(words) >= 2:
            item_name = words[1]

            if "홍" in item_name:
                item_name = item_name[:-1] + "레벨 홍염의 보석"
                # item_name.replace("홍", "레벨 홍염의 보석")
            elif "멸" in item_name:
                item_name = item_name[:-1] + "레벨 멸화의 보석"
                # item_name.replace("멸", "레벨 멸화의 보석")
            else:
                item_name += "레벨"

        if len(words) >= 3:
            class_name = words[2]

        result_items = get_gems(item_name, class_name)["Items"]

        if result_items:
            image_url = result_items[0]["Icon"]

            embed = discord.Embed(
                title=f"{item_name} 검색 결과",
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"{datetime.datetime.now()} 기준", icon_url=icon_url)
            embed.set_thumbnail(url=image_url)

            str_field = ""
            for item in result_items:
                str_field += f'{item["Name"]} {item["AuctionInfo"]["BuyPrice"]}골드\n'

            embed.add_field(name="매물", value=str_field)

            await send_message(message.channel, embed=embed)

        else:
            await send_message(message.channel, message=f"{' '.join(words[1:])}에 해당하는 매물이 없어요")

    async def search_item(self, message):
        keyword = message.content.split()[-1]

        if keyword == "사용법" or keyword == "방법":
            embed = discord.Embed(
                title="아이템 검색 기능 안내",
                url="https://lostarkcodex.com/kr/search/",
                color=discord.Color.blue()
            )

            embed.set_footer(text="2023-01-09 9:30 기준", icon_url=icon_url)

            embed.add_field(name="사용 방법",
                            value=f"1. 아이템 코드 조회\n`Lost Ark Codex`에서 `원하는 아이템의 ID`를 확인합니다\nhttps://lostarkcodex.com/kr/search/\n\n2. 아이템 시세 조회\n`로아 아이템 '아이템ID'`를 입력하여 시세를 확인합니다\n`ex) 아이템 검색 355530118`")

            await send_message(message.channel, embed=embed)

            keyword = '355530118'

        if keyword.isnumeric():
            data = get_markets(int(keyword))

            if data is None:
                await send_message(message.channel, message="해당 아이템은 거래소에서 찾을 수 없습니다")

            else:
                tool_tip = json.loads(data[0]['ToolTip'])

                embed = discord.Embed(
                    title=f"아이템 검색 결과",
                    color=discord.Color.blue()
                )
                embed.set_footer(text=f"{datetime.datetime.now().strftime('%Y/%m/%d %H:%M')} 기준", icon_url=icon_url)

                embed.set_image(
                    url="https://cdn-lostark.game.onstove.com/" + tool_tip["Element_001"]["value"]["slotData"][
                        "iconPath"])

                s = ""
                for key in tool_tip.keys():
                    if tool_tip[key]["type"] == "NameTagBox":
                        continue

                    elif tool_tip[key]["type"] == "ItemTitle":
                        s += self.__get_contents(tool_tip[key]["value"]["leftStr0"])

                    elif tool_tip[key]["type"] == "SingleTextBox":
                        t = tool_tip[key]["value"]

                        content = self.__get_contents(t)

                        if content != "\n" and content != "":
                            s += self.__get_contents(t)

                    elif tool_tip[key]["type"] == "MultiTextBox":
                        continue

                    elif tool_tip[key]["type"] == "ItemPartBox":
                        s += tool_tip[key]["value"]["Element_001"] + "\n"

                    elif tool_tip[key]["type"] == "SymbolString":
                        s += self.__get_contents(tool_tip[key]["value"]["contentStr"])

                    else:
                        print("else:: " + tool_tip[key])

                embed.add_field(name=f"{data[0]['Name']} 정보", value=s)

                s = ""
                for i in range(7):
                    item = data[0]['Stats'][i]
                    s += f"{'-'.join(item['Date'].split('-')[1:])}: {item['AvgPrice']} 골드, {item['TradeCount']}개\n"

                embed.add_field(name=f"{data[0]['Name']} 시세", value=s)

                await send_message(message.channel, embed=embed)

        else:
            await send_message(message.channel, message="잘못된 입력")

    async def show_mari_shop(self, message):
        data = get_mari_shop()

        embed = discord.Embed(
            title=data.title,
            url=data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=data.time + " 기준", icon_url=self.icon_url)

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

        message = await send_message(message.channel, embed=embed, view=options)
        options.set_message(message)

    async def show_gold_info(self, message):
        return await send_message(message.channel, "현재 이용 불가능")

    async def show_search_engraved_info(self, message):
        keyword = message.content.split()[-1]

        data = get_engraving_item(keyword)

        embed = discord.Embed(
            title="전설 각인서 검색 결과",
            color=discord.Color.blue()
        )

        embed.set_footer(icon_url=icon_url)

        if len(data) == 0:
            embed.add_field(name=f"{keyword}", value=f"{keyword} 각인서를 찾을 수 없습니다")
        else:
            for item in data:
                embed.add_field(name=f"{item[1]['Name']}",
                                value=f"{item[1]['Stats'][0]['AvgPrice']} 골드\n거래량 {item[1]['Stats'][0]['TradeCount']}개")

        await send_message(message.channel, embed=embed)

    async def show_occupation_war_info(self, message):
        embed = discord.Embed(
            title="점령전 시간",
            url="https://m-lostark.game.onstove.com/News/Notice/Views/1907?page=1&searchtype=0&searchtext=&noticetype=all",
            color=discord.Color.blue()
        )

        embed.set_footer(text="2022. 3. 30 기준", icon_url=self.icon_url)

        embed.add_field(name="개최 가능 요일", value="목, 금, 토, 일")
        embed.add_field(name="참여 가능 시간", value="12:30 / 16:30 / 18:30 / 19:30 / 22:30 / 23:30")

        await send_message(message.channel, embed=embed)

    async def show_adventure_island_info(self, message):
        difference = 0
        with open(file_dir, "r") as data:
            date = data.read()
            date = datetime.datetime.strptime(date, "%Y-%m-%d")

            difference = datetime.datetime.now() - date

        if difference.days >= 1:
            parse_adventure_island(authorization=self.info['lostark']['apikeyauth'])

            with open(file_dir, "w") as data:
                data.write(datetime.datetime.now().strftime("%Y-%m-%d"))

        now = datetime.datetime.now()
        day = now.weekday()

        link = ""
        if day >= 5:
            link = get_adventure_island(now.strftime("%Y-%m-%d"), True)
        else:
            link = get_adventure_island(now.strftime("%Y-%m-%d"), False)

        embed = discord.Embed(
            title="모험섬",
            url="https://lostark.game.onstove.com/Library/Tip/Views/138208?page=1&libraryStatusType=0&librarySearchCategory=0&searchtype=0&searchtext=&ordertype=latest&LibraryQaAnswerType=None&UserPageType=0",
            color=discord.Color.blue()
        )

        embed.set_footer(text="2021. 7. 10 기준", icon_url=self.icon_url)
        embed.add_field(name="평일", value="11:00 / 13:00 / 19:00 / 21:00 / 23:00")
        embed.add_field(name="주말", value="(오전) 09:00 / 11:00 / 13:00\n(오후) 19:00 / 21:00 / 23:00")

        if link == "":
            await send_message(message.channel, embed=embed)
        else:
            await send_message(message.channel, file=discord.File(link))

    async def show_news(self, message):
        data = get_news()

        if data is None:
            await self.send_specify_message(channel=message.channel, error_name="news_not_found")

        else:
            embeds = []
            for news in data:
                embed = discord.Embed(
                    title=news["Title"],
                    url=news["Link"],
                    color=discord.Color.blue()
                )

                start_date = news["StartDate"].split("T")[0]
                end_date = news["EndDate"].split("T")[0]

                embed.set_image(url=news["Thumbnail"])
                embed.set_footer(text=f"이벤트 기간: {start_date} ~ {end_date}", icon_url=icon_url)

                embeds.append(embed)

                if len(embeds) == 10:
                    await send_message(message.channel, embeds=embeds)
                    embeds.clear()

            if len(embeds) > 0:
                await send_message(message.channel, embeds=embeds)

    async def send_specify_message(self, channel, error_name: str, name: str = ""):
        words = self.__error_messages[error_name]

        message = ""
        for word in words:
            if word.startswith('!'):
                message += name
            else:
                message += word

            message += " "

        await send_message(channel, message)

    def __get_return_words(self, message):
        for item in self.__words["words"]:
            for word in item["trigger_words"]:
                if word in message:
                    return item["return_word"]

        return None
