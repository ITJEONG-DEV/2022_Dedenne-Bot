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
        m += "2파티```fix\n점토 or 회오리 수류탄```\n\n"
        m += "**3페이즈**```fix\n모닥불\n만능 물약\n성스러운 부적\n암흑 or 화염 수류탄```"
        embed.add_field(name="배틀 아이템", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(1페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아르고스",
            description="입장레벨 1370, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "시간 정지 물약",
            "",
            "[자리]",
            "파티 번호 x3",
            "",
            "[작은 피자]",
            "태양 1, 7시/달 11, 5시",
            "```"
        ]
        embed.add_field(name="1페이즈", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(2페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_3(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아르고스",
            description="입장레벨 1370, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템-1파티]",
            "성스러운 부적, 만능 물약, 파괴 폭탄, 화염 수류탄",
            "",
            "[배틀아이템-2파티]",
            "점토 or 회오리 수류탄",
            "",
            "[2-1 페이즈]",
            "브리핑 및 기믹 수행: 외부 안전, 내부 안전, 부분 안전",
            "",
            "[2-2 페이즈]",
            "석상, 바닥패턴, 균열(무력화)",
            "```"
        ]
        embed.add_field(name="2페이즈", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(3페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_4(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아르고스",
            description="입장레벨 1370, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "모닥불, 만능 물약, 성스러운 부적, 암흑 or 화염 수류탄",
            "",
            "[씨앗]",
            "낮: 초록, 밤: 빨강, 새벽: 하양",
            "",
            "[낮 전멸기]",
            "장판 들어가기 / 황금씨앗에서 태양 버프 획득",
            "",
            "[밤 전멸기]",
            "장판 들어가기 / 보라 씨앗 지우기",
            "",
            "[새벽 전멸기]",
            "하얀 씨앗 밟기",
            "```"
        ]
        embed.add_field(name="3페이즈", value="\n".join(m))

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

        m = "**1페이즈**```fix\n회오리 수류탄\n성스러운 부적\n만능 물약```\n\n"
        m += "**2페이즈**```fix\n파괴 폭탄 or 부식 폭탄\n시간 정지 물약```"
        embed.add_field(name="배틀 아이템", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(1페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="발탄(노말/하드)",
            description="입장레벨 1415/1445, 관문 1-2페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "회오리 수류탄, 성스러운 부적, 만능 물약",
            "",
            "[에스더 스킬]",
            "1먹2웨 / 노먹 실리안 등",
            "",
            "[자리]",
            "구슬 먹는 자리 1 ~ 8번",
            "",
            "[45줄] 루가루(빨강) 변신",
            "[40줄] 루카스(파랑) 난입",
            "[33줄] 암흑/감금",
            "[30줄-전멸기] 결속 구슬(무력화)",
            "[25줄] 루가루(빨강) 난입",
            "[15줄-전멸기] 결속 구슬(무력화)",
            "[0-15줄] 공포 무력",
            "```"
        ]
        embed.add_field(name="1페이즈", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(2페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_3(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="발탄(노말/하드)",
            description="입장레벨 1415/1445, 관문 1-2페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "파괴 폭탄(7) or 부식 폭탄(1) / 시간 정지 물약",
            "",
            "[에스더 스킬]",
            "130줄 바훈투르, 16줄 바훈투르, 유령 페이즈-실리안",
            "",
            "[160줄] 갑옷 파괴(박치기)",
            "[130줄-전멸기] 바훈투르, 로나운",
            "[110줄] 임포스터",
            "[88줄] 지형 파괴",
            "[65줄-전멸기] 버러지(카운터)",
            "[30줄] 지형 파괴",
            "[16줄] 4방향 찍기/연한파신권 - 바훈투르",
            "=========================\n"
            "[45줄] 유령 페이즈(카운터)",
            "[39, 27, 14줄-잡기]",
            "```"
        ]
        embed.add_field(name="2페이즈", value="\n".join(m))

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

        m = "**1페이즈**```fix\nn회오리 수류탄\n시간 정지 물약\n신속 로브```\n\n"
        m += "**2페이즈**```fix\nn시간 정지 물약\n신속 로브\n화염 수류탄```\n\n"
        m += "**3페이즈**```fix\nn회오리 수류탄\n시간 정지 물약\n수면 폭탄```"
        embed.add_field(name="배틀 아이템", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(1페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="비아키스(노말/하드)",
            description="입장레벨 1430/1460, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "회오리 수류탄, 시간 정지 물약, 신속 로브",
            "",
            "[에스더 스킬]",
            "욕망 팀 니나브: 아디다스 패턴, 걷어차고 순간이동 위치",
            "",
            "[자리]",
            "구슬 넣기 자리 11, 1, 5, 7시",
            "",
            "[55줄] 쾌락/욕망 파티 분리",
            "[49줄-전멸기] 구슬 드리블(빨파초흰검)",
            "[37줄-전멸기] 구슬 먹기 + 무력 + 내/외부 브리핑",
            "[30줄] 파티 교체",
            "[25줄-전멸기] 안전장판 브리핑",
            "[13줄-전멸기] 구슬 먹기 + 무력 + 내/외부 브리핑"
            ""
            "```"
        ]
        embed.add_field(name="1페이즈", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(2페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_3(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="비아키스(노말/하드)",
            description="입장레벨 1430/1460, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "시간 정지 물약, 신속 로브, 화염 수류탄",
            "",
            "[에스더 스킬]",
            "니나브: 감전 장판, 기절링, 와플 등",
            "",
            "[자리]",
            "보접빨핀 자리: 11, 3, 7 날개와 십자구슬",
            "검빨구슬: 11, 5, 7시 두 명씩 + 스페어 둘",
            "",
            "[145줄] 데칼",
            "[120줄] 보접빨핀",
            "[90줄] 데칼",
            "[65줄] 검빨패턴",
            "```"
        ]
        embed.add_field(name="2페이즈", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(3페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_4(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="비아키스(노말/하드)",
            description="입장레벨 1430/1460, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "회오리 수류탄, 시간 정지 물약, 수면 폭탄",
            "",
            "[에스더 스킬]",
            "135줄 니나브, 0줄 웨이",
            "",
            "[170줄] 늪 패턴",
            "[152줄-전멸기] 칼/석상",
            "[135줄-전멸기] 아재 패턴",
            "[120줄] 매혹 패턴",
            "[102줄-전멸기] 무력 후 시정",
            "[77줄] 늪 패턴",
            "[55줄-전멸기] 촉수 패턴",
            "[37줄(하드)] 욕망구슬 패턴",
            "[0줄] 무력",
            ""
            "```"
        ]
        embed.add_field(name="3페이즈", value="\n".join(m))

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

        m = "**1페이즈**```fix\nn회오리 수류탄\n성스러운 부적\n만능 물약```\n"
        m += "**2페이즈**```fix\nn시간 정지 물약\n암흑 수류탄\n성스러운 폭탄\n성스러운 부적```\n"
        m += "**3페이즈**```fix\nn회오리 수류탄\n성스러운 부적\n만능 물약```"
        embed.add_field(name="배틀 아이템", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(1페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="쿠크세이튼(노말)",
            description="입장레벨 1475, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "회오리 수류탄, 성스러운 부적, 만능 물약",
            "",
            "[에스더 스킬]",
            "니나브: 불 뿜기, 카드마술, 무력 후, 문양 발판, 카운터 직후",
            "",
            "[자리]",
            "세이튼  찾기: 곱3+1",
            "",
            "[주사위 감금 패턴]",
            "- 1인 속박: 3번째 카드가 감금자",
            "- 3인 속박: 속박X인 사람이 1번째 카드",
            "- 같은 색이 연달아 나온다",
            "- (스페이드-하트) / (클로버-다이아)는 짝꿍",
            "",
            "[130줄-전멸기] 방패 피해서 무력화",
            "[110줄-전멸기] 세이튼 찾기",
            "[85줄] 댄스 타임",
            "[60줄-전멸기] 무력화",
            "[50줄] 룰렛",
            "[30줄-전멸기] 세이튼 찾기"
            "```"
        ]
        embed.add_field(name="1페이즈", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(2페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_3(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="쿠크세이튼(노말)",
            description="입장레벨 1475, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "시간 정지 물약, 암흑 수류탄, 성스러운 폭탄, 성스러운 부적",
            "",
            "[에스더 스킬]",
            "니나브, 이난나-벨가 패턴",
            "",
            "[자리]",
            "광기의 장막: 12왼 34오",
            "",
            "[125줄] 세이튼 등장",
            "[110줄] 광기의 장막",
            "[95줄-전멸기] 쿠크 찾기",
            "[80줄-전멸기] 카드 미로 (이난나)",
            "[55줄] 별 패턴(피자)",
            "[25줄-전멸기] 쿠크 찾기"
            "```"
        ]
        embed.add_field(name="2페이즈", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(3페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_4(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="쿠크세이튼(노말)",
            description="입장레벨 1475, 관문 1-3페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "회오리 수류탄, 성스러운 부적, 만능 물약",
            "",
            "[에스더 스킬]",
            "니나브, 이난나-쇼타임, 빙고",
            "",
            "[155줄-전멸기] 1마-톱날",
            "[128줄-전멸기] 2마-갈고리",
            "[90줄-전멸기] 쇼타임 - 어글자 폭탄",
            "[82줄-전멸기] 3마-톱날+갈고리",
            "[55줄-전멸기] 4마-톱날+갈고리+레버",
            "[0줄] 빙고 - 3턴마다 빙고 완성"
            "```"
        ]
        embed.add_field(name="3페이즈", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()


class AbrelshudView(DefaultView):
    def __init__(self, data):
        super().__init__(data)
        self.message = None

    @discord.ui.button(label="레이드 정보", style=discord.ButtonStyle.grey)
    async def on_click_raid_1(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아브렐슈드(노말)",
            description="입장레벨 1490, 관문 1-6페이즈",
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
        m += "**5페이즈**```fix\n시간 정지 물약\n신속 로브\n회오리 수류탄\n```\n"
        m += "**6페이즈**```fix\n시간 정지 물약\n신속 로브\n회오리 or 암흑 수류탄\n```\n"
        embed.add_field(name="배틀 아이템", value=m)

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(1페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아브렐슈드(노말)",
            description="입장레벨 1490, 관문 1-6페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "1파티: 회오리 수류탄, 파괴 폭탄",
            "2파티: 회오리 수류탄, 파괴 폭탄, 상태이상 관련 배틀 아이템",
            "",
            "[에스더 스킬]",
            "실리안: 망치+활 합체 후, 아제나: 잡몹 처리",
            "",
            "[자리]",
            "안전지대: 1파티(곱3), 2파티(곱3+1)",
            "",
            "[투견/석상]",
            "-1파티(슬픔): 투견-파괴, 석상-포도알 드리블",
            "-1파티(절망): 투견-잡몹, 석상-무력화 실패 시 공포",
            "-2파티(분노): 투견-타수, 석상-무력화 시 아군 디버프 제거",
            "-2파티(분노): 투견-무력화, 석상-상태이상 걸어서 디버프 캔슬",
            "",
            "[85줄] 안전지대",
            "[43줄] 카운터 - 아제나",
            "```"
        ]
        embed.add_field(name="1페이즈", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(2페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_3(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아브렐슈드(노말)",
            description="입장레벨 1490, 관문 1-6페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "내부: 점토 수류탄, 수면 폭탄, 시간 정지 물약",
            "외부: 회오리 수류탄",
            "",
            "[에스더 스킬]",
            "실리안, 아제나",
            "",
            "[내부]",
            "-145줄: 보스 모드",
            "-128줄: PVP 모드",
            "-80줄: 보스 모드",
            "-48줄: PVP 모드(강화)",
            "-입장 3회 제한",
            "",
            "[135줄] 주황구슬",
            "[110줄] 빨파장판",
            "[80줄] 무력 후 구슬파괴",
            "[45줄] 빨간 구슬",
            "[40줄] 기사",
            "```"
        ]
        embed.add_field(name="2페이즈", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(3페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_4(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아브렐슈드(노말)",
            description="입장레벨 1490, 관문 1-6페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "회오리 수류탄, 시간 정지 물약, 수면 폭탄, 신속 로브",
            "",
            "[에스더 스킬]",
            "니나브, ",
            "",
            "[미로패턴]",
            "-벽에 닿으면 밀려남",
            "-낙인 생긴 사람은 미니맵의 노란 점으로 탈출",
            "-실패 시 전원 매혹",
            "",
            "[도형 먹이기]",
            "-아슈타로테와 같은 도형 먹이기",
            "-장판에 2인 버프 받기(곱3+1) 혹은 시정",
            "",
            "[145줄] 한컴타자",
            "[100줄] 눈 무력화",
            "[85줄] 광폭화",
            "[42줄] 빨노파 도형 패턴",
            "[0줄] 빨파장판",
            "```"
        ]
        embed.add_field(name="3페이즈", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(4페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_5(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아브렐슈드(노말)",
            description="입장레벨 1490, 관문 1-6페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀아이템]",
            "회오리 or 화염 수류탄, 시간 정지 물약",
            "",
            "[에스더 스킬]",
            "니나브, 웨이, 이난나",
            "",
            "[빨강 큐브]",
            "-전멸기: 헤드방향 피라미드, 무력화",
            "-변형 패턴: 꼭짓점 안전",
            "",
            "[노랑 큐브]",
            "-전멸기: 노란 구슬 터뜨리기, 먹기 / 나머지 무력화",
            "-변형 패턴: 보라색 구슬 생성 후 탄막",
            "",
            "[파랑 큐브]",
            "-전멸기: 2인 4팀 무력화 / 감금 또는 아재패턴",
            "-변형 패턴: 면 부분 외곽 안전",
            "",
            "[170줄-전멸기]",
            "[160줄] 변형",
            "[130줄] 변형",
            "[120줄-전멸기]",
            "[95줄] 무력화",
            "[65줄] 변형",
            "[60줄-전멸기]",
            "[20줄] 무력화",
            "```"
        ]
        embed.add_field(name="4페이즈", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(5페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_6(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아브렐슈드(노말)",
            description="입장레벨 1490, 관문 1-6페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀 아이템]",
            "시간 정지 물약, 신속로브, 회오리 수류탄",
            "",
            "[에스더 스킬]",
            "아제나: 140줄, 110줄 능지, 450줄, 샨디",
            "",
            "[180줄] 도형 생성",
            "[140줄] 블랙홀 설치",
            "[110줄] 무력>큐브>무력>능지",
            "[90줄] 도형 생성",
            "[50줄] 블랙홀 설치",
            "```"
        ]
        embed.add_field(name="5페이즈", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(6페이즈)", style=discord.ButtonStyle.grey)
    async def on_click_raid_7(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="아브렐슈드(노말)",
            description="입장레벨 1490, 관문 1-6페이즈",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "```ini",
            "[배틀 아이템]",
            "시간 정지 물약, 신속로브, 회오리 or 암흑 수류탄",
            "",
            "[에스더 스킬]",
            "188줄: 아제나, 112줄: 아제나 or 샨디, 32줄: 이난나 or 아제나",
            "",
            "[222줄] 블랙홀&화이트홀",
            "[212줄] 몽환 세계",
            "[188줄] 1 운석",
            "[188줄] 맞이하라(메테오)",
            "[137줄] 2 운석",
            "[112줄] 찬미하라",
            "[87줄] 2 운석",
            "[62줄] 블랙홀&화이트홀",
            "[37줄] 4 운석",
            "[32줄] 몽환 세계",
            "[25줄] 추락하라 (타임어택)",
            "```"
        ]
        embed.add_field(name="6페이즈", value="\n".join(m))

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

    @discord.ui.button(label="공략(천공의 문 넬라시아)", style=discord.ButtonStyle.grey)
    async def on_click_raid_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="카양겔(노말/하드I/하드II/하드III)",
            description="입장레벨 1475/1520/1560/1580, 던전",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "<천공의 파수꾼>",
            "```ini",
            "[배틀아이템]",
            "회오리 or 암흑 수류탄, 신속 로브",
            "",
            "[기타 패턴]",
            "- 칼 3개 감금",
            "",
            "[55줄-전멸기] 무력 후 보라or파랑 구슬",
            "[25줄-전멸기] 고리(1-2-3) 부수기",
            "```",
            "<티엔>",
            "```ini",
            "[배틀아이템]",
            "신속 로브",
            "",
            "[빨간 눈 똥]",
            "- 외곽에 장판 빼기",
            "",
            "[55줄-전멸기] 장판 피하기",
            "[30줄] 패턴 강화",
            "```"
        ]
        embed.add_field(name="천공의 문 넬라시아", value="\n".join(m))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="공략(영원한 빛의 요람)", style=discord.ButtonStyle.grey)
    async def on_click_raid_3(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="카양겔(노말/하드I/하드II/하드III)",
            description="입장레벨 1475/1520/1560/1580, 던전",
            color=discord.Color.blue()
        )

        embed.set_footer(text="로스트아크", icon_url=icon_url)

        m = [
            "<프리우나>",
            "```ini",
            "[배틀아이템]",
            "만능 물약, 성스러운 부적, 정화룬/스킬 추천",
            "",
            "[62줄-전멸기] 반시계 상성 오브젝트 파괴",
            "[40줄-전멸기] 기사 카운터 후 무력",
            "[20줄] 색상 띠 위 상성 오브젝트 파괴"
            "```",
            "<라우리엘>",
            "```ini",
            "[배틀아이템]",
            "시간 정지 물약, 화염 or 암흑 수류탄",
            "",
            "[빨간 눈 똥]",
            "- 외곽에 장판 빼기",
            "",
            "[180줄] 결정체 패턴",
            "[140줄] 빛 반사 릴레이",
            "[100줄] 진실의 눈(흰 구슬먹기)",
            "[60줄] 분신 찾기",
            "[컷씬 이후] 강렬한 시선",
            "```"
        ]
        embed.add_field(name="영원한 빛의 요람", value="\n".join(m))

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
