from lostark import Profile, MariShop, GoldInfo
from .. import DBManager

import discord

icon_url = "https://cdn-lostark.game.onstove.com/2018/obt/assets/images/common/icon/favicon-192.png"


class DefaultView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)

        self.message = None
        self.data = data

    def set_message(self, message):
        self.message = message


class CharacterView(DefaultView):
    def __init__(self, data: Profile):
        super().__init__(data)

    @discord.ui.button(label="기본 정보", style=discord.ButtonStyle.grey, emoji="ℹ")
    async def on_click_default_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data.name + "@" + self.data.server + " " + self.data.lv,
            url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
            color=discord.Color.blue()
        )

        embed.set_image(url=self.data.profile_ingame.profile_equipment.src)
        embed.set_footer(text=self.data.name + "\t\t\t" + self.data.time + " 기준", icon_url=self.data.emblem)

        embed.add_field(name="원정대 레벨", value=f"`{self.data.profile_ingame.profile_info.expedition_lv}`")
        embed.add_field(name="아이템 레벨", value=f"`{self.data.profile_ingame.profile_info.equip_item_lv}`")
        embed.add_field(name="영지",
                        value=f"`{self.data.profile_ingame.profile_info.estate_name} {self.data.profile_ingame.profile_info.estate_lv}`")

        m = "```diff\n"
        for slot in self.data.profile_ingame.profile_equipment.ability_engrave_slot.ability:
            if "감소" in str(slot):
                m += "-" + str(slot) + "\n"
            else:
                m += "+" + str(slot) + "\n"
        if m == "```diff\n":
            m = "-"
        else:
            m += "```"
        embed.add_field(name="각인 효과", value=m)

        m = f"공격력 `{self.data.state.attack}\n`최대 생명력 `{self.data.state.hp}`\n"
        embed.add_field(name="기본 특성", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="세트 효과 정보", style=discord.ButtonStyle.grey, emoji="📄")
    async def on_click_set_effect(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data.name + "@" + self.data.server + " " + self.data.lv,
            url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.name + "\t\t\t\t\t\t" + self.data.time + " 기준", icon_url=self.data.emblem)
        embed.set_thumbnail(url=self.data.profile_ingame.profile_equipment.src)

        m = "```"
        for effect in self.data.profile_ingame.profile_equipment.card_slot.effect:
            m += f"{effect.title}\n"
        if m == "```":
            m = "-"
        else:
            m += "```"
        embed.add_field(name="카드 세트 효과", value=m)

        m = "```"
        effect_list = list(self.data.profile_ingame.profile_equipment.equipment_effect_slot)
        effect_list.sort()
        for effect in effect_list:
            m += " ".join(effect.split("\t")[:-1]) + "\n"
        if m == "```":
            m = "-"
        else:
            m += "```"
        embed.add_field(name="장비 세트 효과", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="특성 정보", style=discord.ButtonStyle.grey, emoji="📊")
    async def on_click_ability_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data.name + "@" + self.data.server + " " + self.data.lv,
            url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url=self.data.profile_ingame.profile_equipment.src)
        embed.set_footer(text=self.data.name + "\t\t" + self.data.time + " 기준", icon_url=self.data.emblem)

        m = f"\n치명 `{self.data.state.fatal}`\n특화 `{self.data.state.specialization}`\n제압 `{self.data.state.overpowering}`\n신속 `{self.data.state.swiftness}`\n인내 `{self.data.state.patience}`\n숙련 `{self.data.state.skilled}`"
        embed.add_field(name="전투 특성", value=m)

        state = self.data.profile_state
        m = f"\n지성 `{state.intellect}`\n담력 `{state.courage}`\n매력 `{state.charm}`\n친절 `{state.kindness}`"
        embed.add_field(name="성향", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="보석 정보", style=discord.ButtonStyle.grey, emoji="💎")
    async def on_click_jewel(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data.name + "@" + self.data.server + " " + self.data.lv,
            url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url=self.data.profile_ingame.profile_equipment.src)
        embed.set_footer(text=self.data.name + "\t\t\t\t\t\t\t\t\t\t" + self.data.time + " 기준",
                         icon_url=self.data.emblem)

        m = "```ini\n"
        for jewel in self.data.profile_ingame.profile_equipment.jewel_slot:
            effect = jewel.effect.replace("재사용 대기시간 ", "[쿨타임 -")
            effect = effect.replace(" 감소", "")
            effect = effect.replace("피해 ", "[피해 +")
            effect = effect.replace(" 증가", "")
            effect = effect.replace(".00", "")
            m += f"[{' '.join(jewel.name.split(' ')[:-1])[:-1]}] {jewel.skill_name} {effect}]\n"
        if m == "```md\n":
            m = "-"
        else:
            m += "```"
        embed.add_field(name="보석 정보", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="보유 캐릭터", style=discord.ButtonStyle.grey, emoji="👥")
    async def on_click_character_list(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data.name + "@" + self.data.server + " " + self.data.lv,
            url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.name + "\t\t" + self.data.time + " 기준", icon_url=self.data.emblem)
        embed.set_thumbnail(url=self.data.profile_ingame.profile_equipment.src)

        character_list = self.data.profile_character_list.character_list
        msg = "\n"
        for server in character_list:
            msg += "**" + server.server + "**\n```"
            for character in server.characters:
                msg += character.name + " " + character.lv + " " + character.job + "\n"
            msg += "```\n"

        embed.add_field(name="보유 캐릭터 목록", value=msg)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="내실", style=discord.ButtonStyle.grey, emoji="🌱")
    async def on_click_stability(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data.name + "@" + self.data.server + " " + self.data.lv,
            url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url=self.data.profile_ingame.profile_equipment.src)
        embed.set_footer(text=self.data.name + "\t\t\t\t\t" + self.data.time + " 기준", icon_url=self.data.emblem)

        stability = self.data.profile_stability

        life_skill = stability.profile_skill_life
        embed.add_field(name="생활 스킬", value="\n".join(life_skill.skill))

        collection = stability.profile_collection
        embed.add_field(name="수집형 포인트", value=str(collection))

        await self.message.edit(embed=embed)
        await interaction.response.defer()


class MariShopView(DefaultView):
    def __init__(self, data: MariShop):
        super().__init__(data)

    @discord.ui.button(label="성장 추천", style=discord.ButtonStyle.grey, emoji="🔝")
    async def on_click_tab1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data.title,
            url=self.data.url,
            color=discord.Color.blue()
        )

        # embed.set_footer(text=self.data.name, icon_url=self.data.emblem)
        embed.set_footer(text=self.data.time + " 기준", icon_url=icon_url)

        m = ""
        for i in range(len(self.data.tab1)):
            item = self.data.tab1[i]
            m += f"```diff\n+{item[0]}\n-크리스탈 {item[1]}\n```"
        if m == "":
            m = "현재 판매 상품이 없습니다"
        embed.add_field(name="현재 판매 상품", value=m)

        pre_num = int(len(self.data.tab1_pre) / 6)

        for i in range(pre_num):
            m = ""
            for j in range(6):
                item = self.data.tab1_pre[i * 6 + j]
                m += f"```diff\n+{item[0]}\n-크리스탈 {item[1]}\n```"
            if m == "":
                m = "이전 판매 상품이 없습니다"
            embed.add_field(name=self.data.tab1_pre_name[i], value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="전투ㆍ생활 추천", style=discord.ButtonStyle.grey, emoji="⚔")
    async def on_click_tab2(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data.title,
            url=self.data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.time + " 기준", icon_url=icon_url)

        m = ""
        for i in range(len(self.data.tab2)):
            item = self.data.tab2[i]
            m += f"```diff\n+{item[0]}\n-크리스탈 {item[1]}\n```"
        if m == "":
            m = "현재 판매 상품이 없습니다"
        embed.add_field(name="현재 판매 상품", value=m)

        pre_num = int(len(self.data.tab2_pre) / 6)

        for i in range(pre_num):
            m = ""
            for j in range(6):
                item = self.data.tab2_pre[i * 6 + j]
                m += f"```diff\n+{item[0]}\n-크리스탈 {item[1]}\n```"
            if m == "":
                m = "이전 판매 상품이 없습니다"
            embed.add_field(name=self.data.tab2_pre_name[i], value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()


class GoldView(DefaultView):
    def __init(self, data: GoldInfo):
        super().__init__(data)

    @discord.ui.button(label="골드 시세", style=discord.ButtonStyle.grey, emoji="📉")
    async def on_click_gold(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="골드 시세",
            url=self.data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.time + " 기준", icon_url=icon_url)

        embed.add_field(name="💎골드 팔 때", value=f"```yaml\n{self.data.golds['sell']}\n```")
        embed.add_field(name="💰골드 살 때", value=f"```fix\n{self.data.golds['buy']}\n```")

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="전각 시세 TOP 1-15", style=discord.ButtonStyle.grey, emoji="🥇")
    async def on_click_engraveds_1(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="전설 각인서 시세",
            url=self.data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.time + " 기준", icon_url=icon_url)

        engraveds = []
        for i in range(0, 15):
            engraveds.append("%02d. " % (i + 1) + str(self.data.engraveds[i]))

        embed.add_field(name="전각 시세 TOP 1-15", value="\n".join(engraveds))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="전각 시세 TOP 16-40", style=discord.ButtonStyle.grey, emoji="🥈")
    async def on_click_engraveds_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="전설 각인서 시세",
            url=self.data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.time + " 기준", icon_url=icon_url)

        engraveds = []
        for i in range(16, 40):
            engraveds.append("%02d. " % (i + 1) + str(self.data.engraveds[i]))

        embed.add_field(name="전각 시세 TOP 16-40", value="\n".join(engraveds))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="전각 시세 TOP 41-65", style=discord.ButtonStyle.grey, emoji="🥉")
    async def on_click_engraveds_3(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="전설 각인서 시세",
            url=self.data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.time + " 기준", icon_url=icon_url)

        engraveds = []
        for i in range(41, 65):
            engraveds.append("%02d. " % (i + 1) + str(self.data.engraveds[i]))

        embed.add_field(name="전각 시세 TOP 41-65", value="\n".join(engraveds))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="전각 시세 TOP 65-", style=discord.ButtonStyle.grey, emoji="🎖")
    async def on_click_engraveds_4(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="전설 각인서 시세",
            url=self.data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.time + " 기준", icon_url=icon_url)

        engraveds = []
        for i in range(65, len(self.data.engraveds)):
            engraveds.append("%02d. " % (i + 1) + str(self.data.engraveds[i]))

        embed.add_field(name="전각 시세 TOP 51-", value="\n".join(engraveds))

        await self.message.edit(embed=embed)
        await interaction.response.defer()


class RaidView(DefaultView):
    def __init__(self, data):
        super().__init__(data)
        self.message = None

    @discord.ui.button(label="아르고스", style=discord.ButtonStyle.grey)
    async def on_click_raid_1(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아르고스",
            description="입장레벨 1370, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = "```diff\n+1600 골드```"
        embed.add_field(name="골드 보상", value=m)

        m = "```diff\n-500 골드```"
        embed.add_field(name="더보기 골드", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="발탄", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
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

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="비아키스", style=discord.ButtonStyle.grey)
    async def on_click_raid_3(self, interaction: discord.Interaction, button: discord.ui.button()):
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

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="쿠크세이튼", style=discord.ButtonStyle.grey)
    async def on_click_raid_4(self, interaction: discord.Interaction, button: discord.ui.button()):
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

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="아브렐슈드", style=discord.ButtonStyle.grey)
    async def on_click_raid_5(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아브렐슈드(노말/하드)",
            description="입장레벨 1490/1540, 관문 1-6페이즈",
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

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="카양겔", style=discord.ButtonStyle.grey)
    async def on_click_raid_6(self, interaction: discord.Interaction, button: discord.ui.button()):
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

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="일리아칸", style=discord.ButtonStyle.grey)
    async def on_click_raid_7(self, interaction: discord.Interaction, button: discord.ui.button()):
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

        await self.message.edit(embed=embed)
        await interaction.response.defer()


class ArgosView(DefaultView):
    def __init__(self, data):
        super().__init__(data)
        self.message = None

    @discord.ui.button(label="레이드 정보", style=discord.ButtonStyle.grey)
    async def on_click_raid_1(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아르고스",
            description="입장레벨 1370, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = "\n**1페이즈**```fix\n시간 정지 물약```\n\n"
        m += "**2페이즈**\n"
        m += "1파티```fix\n성스러운 부적\n만능 물약\n파괴 폭탄\n화염 수류탄```\n"
        m += "2파티```fix\n점토 수류탄 or 회오리 수류탄```\n\n"
        m += "**3페이즈**```fix\n모닥불\n만능 물약\n성스러운 부적\n암흑 수류탄 or 화염 수류탄```"
        embed.add_field(name="배틀 아이템", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(준비중)", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아르고스",
            description="입장레벨 1370, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        await self.message.edit(embed=embed)
        await interaction.response.defer()


class BaltanView(DefaultView):
    def __init__(self, data):
        super().__init__(data)
        self.message = None

    @discord.ui.button(label="레이드 정보", style=discord.ButtonStyle.grey)
    async def on_click_raid_1(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="발탄(노말/하드)",
            description="입장레벨 1415/1445, 관문 1-2페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = "**1페이즈**```fix\n물약\n회오리 수류탄\n성스러운 부적\n만능 물약```\n\n"
        m += "**2페이즈**```fix\n물약\n파괴 폭탄 or 부식 폭탄\n시간 정지 물약```"
        embed.add_field(name="배틀 아이템", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(준비중)", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="발탄(노말/하드)",
            description="입장레벨 1415/1445, 관문 1-2페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        await self.message.edit(embed=embed)
        await interaction.response.defer()


class BiackissView(DefaultView):
    def __init__(self, data):
        super().__init__(data)
        self.message = None

    @discord.ui.button(label="레이드 정보", style=discord.ButtonStyle.grey)
    async def on_click_raid_1(self, interaction: discord.Interaction, button: discord.ui.button()):
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

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(준비중)", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="비아키스(노말/하드)",
            description="입장레벨 1430/1460, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        await self.message.edit(embed=embed)
        await interaction.response.defer()


class KoukuSatonView(DefaultView):
    def __init__(self, data):
        super().__init__(data)
        self.message = None

    @discord.ui.button(label="레이드 정보", style=discord.ButtonStyle.grey)
    async def on_click_raid_1(self, interaction: discord.Interaction, button: discord.ui.button()):
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

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(준비중)", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="쿠크세이튼(노말)",
            description="입장레벨 1475, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        await self.message.edit(embed=embed)
        await interaction.response.defer()


class AbrelshudView(DefaultView):
    def __init__(self, data):
        super().__init__(data)
        self.message = None

    @discord.ui.button(label="레이드 정보", style=discord.ButtonStyle.grey)
    async def on_click_raid_1(self, interaction: discord.Interaction, button: discord.ui.button()):
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

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(준비중)", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아브렐슈드(노말/하드)",
            description="입장레벨 1490/1540, 관문 1-6페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        await self.message.edit(embed=embed)
        await interaction.response.defer()


class KayangelView(DefaultView):
    def __init__(self, data):
        super().__init__(data)
        self.message = None

    @discord.ui.button(label="레이드 정보", style=discord.ButtonStyle.grey)
    async def on_click_raid_1(self, interaction: discord.Interaction, button: discord.ui.button()):
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

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(준비중)", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="카양겔(노말/하드I/하드II/하드III)",
            description="입장레벨 1475/1520/1560/1580, 던전",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        await self.message.edit(embed=embed)
        await interaction.response.defer()


class IlliakanView(DefaultView):
    def __init__(self, data):
        super().__init__(data)
        self.message = None

    @discord.ui.button(label="레이드 정보", style=discord.ButtonStyle.grey)
    async def on_click_raid_1(self, interaction: discord.Interaction, button: discord.ui.button()):
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

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(준비중)", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="일리아칸(노말/하드)",
            description="입장레벨 1580/1600, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        await self.message.edit(embed=embed)
        await interaction.response.defer()
