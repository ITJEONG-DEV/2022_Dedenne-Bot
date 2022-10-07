import datetime

from bot.botWorker import *
from data import *
from util import parse_json

from lostark import get_character_data, get_mari_shop, get_gold_info
from bot.view import *

from . import DBManager

import discord

KOREA = datetime.timezone(datetime.timedelta(hours=9))

ready = False


class DedenneBot(discord.Client):
    async def on_ready(self):
        # word profile
        self.__words = parse_json("json/command_collection.json")
        self.__error_messages = parse_json("json/error_messages.json")

        # bot worker
        self.__worker = BotWorker(self)

        # db manager
        self.__db = DBManager()

        self.icon_url = "https://cdn-lostark.game.onstove.com/2018/obt/assets/images/common/icon/favicon-192.png"

        print('Logged on as', self.user)

        global ready
        ready = True

    async def on_message(self, message):
        await self.wait_until_ready()

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
                await self.send_message(message.channel, content)

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

                elif content == "search-engraved":
                    await self.show_search_engraved_info(message)

                elif content == "engraved":
                    await self.show_engraved_info(message)

                elif content == "occupation-war":
                    await self.show_occupation_war_info(message)

                # 레이드 공략

                elif content == "argos-solution":
                    await self.show_argos_solution(message)

                elif content == "baltan-solution":
                    await self.show_baltan_solution(message)

                elif content == "biackiss-solution":
                    await self.show_biackiss_solution(message)

                elif content == "kouku-saton-solution":
                    await self.show_kouku_saton_solution(message)

                elif content == "abrelshud-solution":
                    await self.show_abrelshud_solution(message)

                elif content == "kayangel-solution":
                    await self.show_kayangel_solution(message)

                elif content == "illiakan-solution":
                    await self.show_illiakan_solution(message)

                # 레이드 보상

                elif content == "raid":
                    await self.show_raid_info(message)

                elif content == "baltan":
                    await self.show_baltan_info(message)

                elif content == "biackiss":
                    await self.show_biackiss_info(message)

                elif content == "kouku-saton":
                    await self.show_kouku_saton_info(message)

                elif content == "abrelshud":
                    await self.show_abrelshud_info(message)

                elif content == "kayangel":
                    await self.show_kayangel_info(message)

                elif content == "illiakan":
                    await self.show_illiakan_info(message)

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

        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_gold_info(self, message):
        data = get_gold_info()

        embed = discord.Embed(
            title="골드 시세",
            url=data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=data.time + " 기준", icon_url=self.icon_url)

        embed.add_field(name="💎골드 팔 때", value=f"```yaml\n{data.golds['sell']}\n```")
        embed.add_field(name="💰골드 살 때", value=f"```fix\n{data.golds['buy']}\n```")

        options = GoldView(data=data)

        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_search_engraved_info(self, message):
        keyword = message.content.split()[-1]

        keyword_dict = {
            "구동": "구슬동자",
            "강무": "강화 무기",
            "결대": "결투의 대가",
            "극의체술": "극의:",
            "급타": "급소타격",
            "고기": "고독한 기사",
            "기대": "기습의 대가",
            "달소": "달의 소리",
            "달저": "달인의 저력",
            "돌대": "돌격대장",
            "마효증": "마나 효율 증가",
            "마흐": "마나의 흐름",
            "부뼈": "부러진 뼈",
            "분망": "분노의 망치",
            "번분": "번개의 분노",
            "사시": "사냥의 시간",
            "선필": "선수필승",
            "시집": "시선 집중",
            "아기": "아르데타인의 기술",
            "안상": "안정된 상태",
            "약무": "약자 무시",
            "예둔": "예리한 둔기",
            "저받": "저주받은",
            "전태": "전투 태세",
            "절구": "절실한 구원",
            "정단": "정밀 단도",
            "정흡": "정기 흡수",
            "중수": "중력 수련",
            "중착": "중갑 착용",
            "진용": "진실된 용맹",
            "질증": "질량 증가",
            "최마증": "최대 마나 증가",
            "충단": "충격 단련",
            "타대": "타격의 대가",
            "폭전": "폭발물 전문가",
            "피메": "피스메이커"
        }

        data = get_gold_info()

        embed = discord.Embed(
            title="전설 각인서 검색",
            url=data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=data.time + " 기준", icon_url=icon_url)

        if keyword in keyword_dict.keys():
            keyword = keyword_dict[keyword]

        target = None
        for engraved in data.engraveds:
            if keyword in engraved.name:
                target = engraved

        if target is None:
            embed.add_field(name=f"{keyword}", value=f"{keyword} 각인서를 찾을 수 없습니다")
        else:
            embed.add_field(name=f"{target.name}", value=f"{target.price} 골드")

        await message.channel.send(embed=embed)

    async def show_engraved_info(self, message):
        data = get_gold_info()

        embed = discord.Embed(
            title="전설 각인서 시세",
            url=data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=data.time + " 기준", icon_url=icon_url)

        engraveds = []
        for i in range(0, 15):
            engraveds.append("%02d. " % (i + 1) + str(data.engraveds[i]))

        embed.add_field(name="전각 시세 TOP 1-15", value="\n".join(engraveds))

        options = GoldView(data=data)

        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_occupation_war_info(self, message):
        embed = discord.Embed(
            title="점령전 시간",
            url="https://m-lostark.game.onstove.com/News/Notice/Views/1907?page=1&searchtype=0&searchtext=&noticetype=all",
            color=discord.Color.blue()
        )

        embed.set_footer(text="2022. 3. 30 기준", icon_url=self.icon_url)

        embed.add_field(name="개최 가능 요일", value="목, 금, 토, 일")
        embed.add_field(name="참여 가능 시간", value="12:30 / 16:30 / 18:30 / 19:30 / 22:30 / 23:30")

        await message.channel.send(embed=embed)

    async def show_argos_solution(self, message):
        embed = discord.Embed(
            title="아르고스",
            description="입장레벨 1370, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = "\n**1페이즈**```fix\n시간 정지 물약```\n\n"
        m += "**2페이즈**\n"
        m += "1파티```fix\n성스러운 부적\n만능 물약\n파괴 폭탄\n화염 수류탄```\n"
        m += "2파티```fix\n점토 수류탄 or 회오리 수류탄```\n\n"
        m += "**3페이즈**```fix\n모닥불\n만능 물약\n성스러운 부적\n암흑 수류탄 or 화염 수류탄```"
        embed.add_field(name="배틀 아이템", value=m)

        options = ArgosView(data=None)
        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_baltan_solution(self, message):
        embed = discord.Embed(
            title="발탄(노말/하드)",
            description="입장레벨 1415/1445, 관문 1-2페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = "**1페이즈**```fix\n물약\n회오리 수류탄\n성스러운 부적\n만능 물약```\n\n"
        m += "**2페이즈**```fix\n물약\n파괴 폭탄 or 부식 폭탄\n시간 정지 물약```"
        embed.add_field(name="배틀 아이템", value=m)

        options = BaltanView(data=None)
        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_biackiss_solution(self, message):
        embed = discord.Embed(
            title="비아키스(노말/하드)",
            description="입장레벨 1430/1460, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = "**1페이즈**```fix\n물약\n회오리 수류탄\n시간 정지 물약\n신속 로브```\n\n"
        m += "**2페이즈**```fix\n물약\n시간 정지 물약\n신속 로브\n화염 수류탄```\n\n"
        m += "**3페이즈**```fix\n물약\n회오리 수류탄\n시간 정지 물약\n수면 폭탄```"
        embed.add_field(name="배틀 아이템", value=m)

        options = BiackissView(data=None)
        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_kouku_saton_solution(self, message):
        embed = discord.Embed(
            title="쿠크세이튼(노말)",
            description="입장레벨 1475, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = "**1페이즈**```fix\n물약\n회오리 수류탄\n성스러운 부적\n만능 물약```\n"
        m += "**2페이즈**```fix\n물약\n시간 정지 물약\n암흑 수류탄\n성스러운 폭탄```\n"
        m += "**3페이즈**```fix\n물약\n회오리 수류탄\n성스러운 부적\n만능 물약```"
        embed.add_field(name="배틀 아이템", value=m)

        options = KoukuSatonView(data=None)
        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_abrelshud_solution(self, message):
        embed = discord.Embed(
            title="아브렐슈드(노말/하드)",
            description="입장레벨 1490/1540, 관문 1-6페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = "**1페이즈**\n"
        m += "<1파티>```fix\n회오리 수류탄\n파괴 폭탄\n```\n"
        m += "<2파티>```fix\n회오리 수류탄\n파괴 폭탄\n상태이상 관련 배틀 아이템```\n"
        m += "**2페이즈**\n"
        m += "<내부>```fix\n점토 수류탄\n수면 폭탄\n시간 정지 물약\n```\n"
        m += "<외부>```fix\n회오리 수류탄\n```\n"
        m += "**3페이즈**```fix\n회오리 수류탄\n시간 정지 물약\n수면 폭탄\n신속 로브```\n"
        m += "**4페이즈**```fix\n회오리 or 화염 수류탄\n시간 정지 물약\n```\n"
        m += "**5페이즈**```fix\n시간 정지 물약\n회오리 수류탄\n```\n"
        m += "**6페이즈**```fix\n시간 정지 물약\n회오리 or 암흑 수류탄\n```\n"
        embed.add_field(name="배틀 아이템", value=m)

        options = AbrelshudView(data=None)
        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_kayangel_solution(self, message):
        embed = discord.Embed(
            title="카양겔(노말/하드I/하드II/하드III)",
            description="입장레벨 1475/1520/1560/1580, 던전",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = "**천공의 문 넬라시아**\n\n"
        m += "<천공의 파수꾼>```fix\n회오리 or 암흑 수류탄\n신속 로브```\n"
        m += "<티엔>```fix\n신속 로브```\n\n"
        m += "**영원한 빛의 요람**\n\n"
        m += "<프리우나>```fix\n만능 물약\n성스러운 부적```\n"
        m += "<라우리엘>```fix\n시간 정지 물약\n화염 or 암흑 수류탄```\n"

        embed.add_field(name="배틀 아이템", value=m)

        options = KayangelView(data=None)
        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_illiakan_solution(self, message):
        embed = discord.Embed(
            title="일리아칸(노말/하드)",
            description="입장레벨 1580/1600, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = "**1페이즈**```fix\n물약\n성스러운 부적\n만능 물약\n회오리 or 암흑 수류탄```\n"
        m += "**2페이즈**```fix\n물약\n부식 or 파괴 폭탄\n암흑 수류탄\n진군의 깃발 or 성스러운 부적```\n"
        m += "**3페이즈**```fix\n물약\n회오리 수류탄\n파괴 폭탄\n성스러운 부적```"
        embed.add_field(name="배틀 아이템", value=m)

        options = IlliakanView(data=None)
        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_raid_info(self, message):
        embed = discord.Embed(
            title="아르고스",
            description="입장레벨 1370, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=self.icon_url)

        m = "```diff\n수호석 결정 240개\n파괴석 결정 120개\n명예의 파편 720개\n위대한 명예의 돌파석 5개\n+1600 골드```"
        embed.add_field(name="레이드 보상", value=m)

        m = "```diff\n수호석 결정 240개\n파괴석 결정 120개\n명예의 파편 720개\n위대한 명예의 돌파석 5개\n-500 골드```"
        embed.add_field(name="더보기 보상", value=m)

        options = RaidView(data=None)
        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_baltan_info(self, message):
        embed = discord.Embed(
            title="발탄(노말/하드)",
            description="입장레벨 1415/1445, 관문 1-2페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        item = "마수의 뼈"

        m = f"1관문(1415)```diff\n+500 골드\n-500 골드\n{item} 1개```"
        m += f"2관문(1415)```diff\n+2000 골드\n-800 골드\n{item} 2개```"
        m += f"총계```diff\n+2500 골드\n-1300 골드\n{item} 3개```"
        embed.add_field(name="발탄(노말)", value=m)

        m = f"1관문(1445)```diff\n+1000 골드\n-900 골드\n{item} 3개```"
        m += f"2관문(1445)```diff\n+3500 골드\n-1200 골드\n{item} 3개```"
        m += f"총계```diff\n+4500 골드\n-2100 골드\n{item} 6개```"
        embed.add_field(name="발탄(하드)", value=m)

        options = BaltanView(data=None)
        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_biackiss_info(self, message):
        embed = discord.Embed(
            title="비아키스(노말/하드)",
            description="입장레벨 1430/1460, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        item = "욕망의 날개"

        m = f"1관문(1430)```diff\n+500 골드\n-400 골드\n{item} 1개```"
        m += f"2관문(1430)```diff\n+600 골드\n-600 골드\n{item} 1개```"
        m += f"3관문(1430)```diff\n+1400 골드\n-800 골드\n{item} 1개```"
        m += f"총계```diff\n+2500 골드\n-1800 골드\n{item} 3개```"
        embed.add_field(name="비아키스(노말)", value=m)

        m = f"1관문(1460)```diff\n+1000 골드\n-700 골드\n{item} 2개```"
        m += f"2관문(1460)```diff\n+1000 골드\n-900 골드\n{item} 2개```"
        m += f"3관문(1460)```diff\n+2500 골드\n-1200 골드\n{item} 2개```"
        m += f"총계```diff\n+4500 골드\n-2800 골드\n{item} 6개```"
        embed.add_field(name="비아키스(하드)", value=m)

        options = RaidView(data=None)
        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_kouku_saton_info(self, message):
        embed = discord.Embed(
            title="쿠크세이튼(노말)",
            description="입장레벨 1475, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        item = "광기의 나팔"

        m = f"1관문(1475)```diff\n+1000 골드\n-800 골드\n{item} 1개```"
        m += f"2관문(1475)```diff\n+1000 골드\n-1000 골드\n{item} 2개```"
        m += f"3관문(1475)```diff\n+2500 골드\n-1300 골드\n{item} 2개\n에스더의 기운(낮은 확률)```"
        m += f"총계```diff\n+4500 골드\n-3100 골드\n{item} 5개```"
        embed.add_field(name="쿠크세이튼(노말)", value=m)

        options = RaidView(data=None)
        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_abrelshud_info(self, message):
        embed = discord.Embed(
            title="아브렐슈드(노말/하드)",
            description="입장레벨 1490/1540, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        item = "몽환의 뿔"

        m = f"1관문(1490)```diff\n+2000 골드\n-400 골드\n{item} 3개```"
        m += f"2관문(1490)```diff\n+2500 골드\n-600 골드\n{item} 4개```"
        m += f"3관문(1500)```diff\n+700 골드\n-700 골드\n{item} 3개```"
        m += f"4관문(1500)```diff\n+800 골드\n-800 골드\n{item} 4개```"
        m += f"5관문(1520)```diff\n+1000 골드\n-900 골드\n{item} 3개```"
        m += f"6관문(1520)```diff\n+1500 골드\n-1100 골드\n{item} 5개\n에스더의 기운(낮은 확률)```"
        m += f"총계```diff\n+8500 골드\n-4500 골드\n{item} 22개```"
        embed.add_field(name="아브렐슈드(노말)", value=m)

        item = "몽환의 사념"

        m = f"1관문(1540)```diff\n+2500 골드\n-700 골드\n{item} 3개```"
        m += f"2관문(1540)```diff\n+3000 골드\n-800 골드\n{item} 4개```"
        m += f"3관문(1550)```diff\n+900 골드\n-900 골드\n{item} 3개```"
        m += f"4관문(1550)```diff\n+1100 골드\n-1100 골드\n{item} 4개```"
        m += f"5관문(1560)```diff\n+1200 골드\n-1100 골드\n{item} 3개```"
        m += f"6관문(1560)```diff\n+1800 골드\n-1400 골드\n{item} 5개\n에스더의 기운(낮은 확률)```"
        m += f"총계```diff\n+10500 골드\n-6000 골드\n{item} 22개```"
        embed.add_field(name="아브렐슈드(하드)", value=m)

        options = RaidView(data=None)
        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_kayangel_info(self, message):
        embed = discord.Embed(
            title="카양겔(노말/하드I/하드II/하드III)",
            description="입장레벨 1475/1520/1560/1580, 던전",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        # 노말
        m = f"천공의 문 넬라시아```diff\n파괴석 결정 800개\n수호석 결정 1600개\n명예의 파편 2400개\n위대한 명예의 돌파석 0개\n시련의 빛 8개\n+0 골드```"
        m += f"영원한 빛의 요람```diff\n파괴석 결정 1200개\n수호석 결정 2400개\n명예의 파편 3000개\n위대한 명예의 돌파석 0개\n시련의 빛 12개\n+0 골드```"
        embed.add_field(name="카양겔(노말) 클리어 보상", value=m)

        m = f"천공의 문 넬라시아```diff\n파괴석 결정 420개\n수호석 결정 840개\n명예의 파편 1400개\n위대한 명예의 돌파석 12개\n시련의 빛 8개\n-400 골드```"
        m += f"영원한 빛의 요람```diff\n파괴석 결정 540개\n수호석 결정 1080개\n명예의 파편 1600개\n위대한 명예의 돌파석 12개\n시련의 빛 12개\n-600 골드```"
        embed.add_field(name="카양겔(노말) 더보기 보상", value=m)

        m = f"천공의 문 넬라시아```diff\n파괴석 결정 1220개\n수호석 결정 2440개\n명예의 파편 3800개\n위대한 명예의 돌파석 12개\n시련의 빛 8개\n-400 골드```"
        m += f"영원한 빛의 요람```diff\n파괴석 결정 1740개\n수호석 결정 3480개\n명예의 파편 4600개\n위대한 명예의 돌파석 12개\n시련의 빛 24개\n-600 골드```"
        embed.add_field(name="카양겔(노말) 총계", value=m)

        # 하드 1
        m = f"천공의 문 넬라시아```diff\n파괴강석 360개\n수호강석 720개\n명예의 파편 3600개\n경이로운 명예의 돌파석 0개\n시련의 빛 13개\n+0골드```"
        m += f"영원한 빛의 요람```diff\n파괴강석 380개\n수호강석 760개\n명예의 파편 4000개\n경이로운 명예의 돌파석 0개\n심화 돌파석 12개\n시련의 빛 17개\n+0 골드```"
        embed.add_field(name="카양겔(하드I) 클리어 보상", value=m)

        m = f"천공의 문 넬라시아```diff\n파괴강석 100개\n수호강석 200개\n명예의 파편 1400개\n경이로운 명예의 돌파석 4개\n시련의 빛 13개\n-700 골드```"
        m += f"영원한 빛의 요람```diff\n파괴강석 140개\n수호강석 280개\n명예의 파편 1600개\n경이로운 명예의 돌파석 6개\n심화 돌파석 6개\n시련의 빛 17개\n-800 골드```"
        embed.add_field(name="카양겔(하드I) 더보기 보상", value=m)

        m = f"천공의 문 넬라시아```diff\n파괴강석 460개\n수호강석 920개\n명예의 파편 5000개\n경이로운 명예의 돌파석 4개\n시련의 빛 26개\n-700 골드```"
        m += f"영원한 빛의 요람```diff\n파괴강석 520개\n수호강석 1040개\n명예의 파편 5600개\n경이로운 명예의 돌파석 6개\n심화 돌파석 18개\n시련의 빛 34개\n-800 골드\n에스더의 기운(낮은 확률)```"
        embed.add_field(name="카양겔(하드I) 총계", value=m)

        # 하드 2
        m = f"천공의 문 넬라시아```diff\n파괴강석 400개\n수호강석 800개\n명예의 파편 4000개\n경이로운 명예의 돌파석 0개\n시련의 빛 18개\n관조의 빛무리 1개\n+0골드```"
        m += f"영원한 빛의 요람```diff\n파괴강석 480개\n수호강석 960개\n명예의 파편 5000개\n경이로운 명예의 돌파석 0개\n심화 돌파석 15개\n시련의 빛 22개\n관조의 빛무리 1개\n+0 골드```"
        embed.add_field(name="카양겔(하드II) 클리어 보상", value=m)

        m = f"천공의 문 넬라시아```diff\n파괴강석 180개\n수호강석 360개\n명예의 파편 1600개\n경이로운 명예의 돌파석 8개\n시련의 빛 18개\n관조의 빛무리 1개\n-900 골드```"
        m += f"영원한 빛의 요람```diff\n파괴강석 240개\n수호강석 480개\n명예의 파편 2000개\n경이로운 명예의 돌파석 8개\n심화 돌파석 8개\n시련의 빛 22개\n관조의 빛무리 1개\n-1100 골드```"
        embed.add_field(name="카양겔(하드II) 더보기 보상", value=m)

        m = f"천공의 문 넬라시아```diff\n파괴강석 580개\n수호강석 1160개\n명예의 파편 5600개\n경이로운 명예의 돌파석 8개\n시련의 빛 36개\n관조의 빛무리 2개\n-900 골드```"
        m += f"영원한 빛의 요람```diff\n파괴강석 720개\n수호강석 1440개\n명예의 파편 7000개\n경이로운 명예의 돌파석 8개\n심화 돌파석 23개\n시련의 빛 44개\n관조의 빛무리 2개\n-1100 골드\n에스더의 기운(낮은 확률)```"
        embed.add_field(name="카양겔(하드II) 총계", value=m)

        # 하드 3
        m = f"천공의 문 넬라시아```diff\n파괴강석 600개\n수호강석 1200개\n명예의 파편 5000개\n경이로운 명예의 돌파석 0개\n시련의 빛 20개\n관조의 빛무리 2개\n+0골드```"
        m += f"영원한 빛의 요람```diff\n파괴강석 780개\n수호강석 1560개\n명예의 파편 6400개\n경이로운 명예의 돌파석 0개\n심화 돌파석 20개\n시련의 빛 30개\n관조의 빛무리 3개\n+0 골드```"
        embed.add_field(name="카양겔(하드III) 클리어 보상", value=m)

        m = f"천공의 문 넬라시아```diff\n파괴강석 300개\n수호강석 600개\n명예의 파편 2400개\n경이로운 명예의 돌파석 10개\n시련의 빛 20개\n관조의 빛무리 2개\n-1100 골드```"
        m += f"영원한 빛의 요람```diff\n파괴강석 450개\n수호강석 900개\n명예의 파편 3000개\n경이로운 명예의 돌파석 15개\n심화 돌파석 10개\n시련의 빛 30개\n관조의 빛무리 3개\n-1400 골드```"
        embed.add_field(name="카양겔(하드III) 더보기 보상", value=m)

        m = f"천공의 문 넬라시아```diff\n파괴강석 900개\n수호강석 1800개\n명예의 파편 7400개\n경이로운 명예의 돌파석 10개\n시련의 빛 40개\n관조의 빛무리 4개\n-1100 골드```"
        m += f"영원한 빛의 요람```diff\n파괴강석 1230개\n수호강석 2460개\n명예의 파편 9400개\n경이로운 명예의 돌파석 15개\n심화 돌파석 30개\n시련의 빛 60개\n관조의 빛무리 6개\n-1400 골드\n에스더의 기운(낮은 확률)\n에스더 탈 것: 고요의 날개, 금기의 날개```"
        embed.add_field(name="카양겔(하드III) 총계", value=m)

        options = RaidView(data=None)
        message = await message.channel.send(embed=embed, view=options)
        options.set_message(message)

    async def show_illiakan_info(self, message):
        embed = discord.Embed(
            title="일리아칸(노말/하드)",
            description="입장레벨 1580/1600, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        item = "쇠락의 눈동자"

        m = f"1관문(1580)```diff\n+1500 골드\n-900 골드\n{item} 3개```"
        m += f"2관문(1580)```diff\n+1750 골드\n-1100 골드\n{item} 3개```"
        m += f"3관문(1580)```diff\n+2250 골드\n-1500 골드\n{item} 5개```"
        m += f"총계```diff\n+5500 골드\n-3500 골드\n{item} 11개```"
        embed.add_field(name="일리아칸(노말)", value=m)

        m = f"1관문(1600)```diff\n+1750 골드\n-1200 골드\n{item} 7개```"
        m += f"2관문(1600)```diff\n+2000 골드\n-1400 골드\n{item} 7개```"
        m += f"3관문(1600)```diff\n+2750 골드\n-1900 골드\n{item} 8개```"
        m += f"총계```diff\n+5500 골드\n-4500 골드\n{item} 22개```"
        embed.add_field(name="일리아칸(하드)", value=m)

        options = RaidView(data=None)
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
