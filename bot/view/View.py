from lostark import Profile, MariShop, GoldInfo

import discord


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

        embed.add_field(name="원정대 레벨", value=self.data.profile_ingame.profile_info.expedition_lv)
        embed.add_field(name="아이템 레벨", value=self.data.profile_ingame.profile_info.equip_item_lv)
        embed.add_field(name="영지",
                        value=f"**{self.data.profile_ingame.profile_info.estate_name}  {self.data.profile_ingame.profile_info.estate_lv}**")

        m = ""
        for slot in self.data.profile_ingame.profile_equipment.ability_engrave_slot.ability:
            m += str(slot) + "\n"
        if m == "":
            m = "-"
        embed.add_field(name="각인 효과", value=m)

        m = f"공격력 {self.data.state.attack}\n최대 생명력 {self.data.state.hp}"
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

        m = ""
        for effect in self.data.profile_ingame.profile_equipment.card_slot.effect:
            m += f"{effect.title}\n"
        if m == "":
            m = "-"
        embed.add_field(name="카드 세트 효과", value=m)

        m = ""
        effect_list = list(self.data.profile_ingame.profile_equipment.equipment_effect_slot)
        effect_list.sort()
        for effect in effect_list:
            m += " ".join(effect.split("\t")[:-1]) + "\n"
        if m == "":
            m = "-"
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

        m = f"치명 {self.data.state.fatal}\n특화 {self.data.state.specialization}\n제압 {self.data.state.overpowering}\n신속 {self.data.state.swiftness}\n인내 {self.data.state.patience}\n숙련 {self.data.state.skilled}"
        embed.add_field(name="전투 특성", value=m)

        state = self.data.profile_state
        m = f"지성 {state.intellect}\n담력 {state.courage}\n매력 {state.charm}\n친절 {state.kindness}\n"
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

        m = ""
        for jewel in self.data.profile_ingame.profile_equipment.jewel_slot:
            m += f"{jewel.name} {jewel.skill_name} {jewel.effect}\n"
        if m == "":
            m = "-"
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

        embed.set_footer(text=self.data.name + "\t\t\t" + self.data.time + " 기준", icon_url=self.data.emblem)
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
        embed.set_footer(text=self.data.time + " 기준")

        m = ""
        for i in range(len(self.data.tab1)):
            item = self.data.tab1[i]
            m += f"{i + 1}. {item[0]} 크리스탈 {item[1]}\n"
        if m == "":
            m = "현재 판매 상품이 없습니다"
        embed.add_field(name="현재 판매 상품", value=m)

        pre_num = int(len(self.data.tab1_pre) / 6)

        for i in range(pre_num):
            m = ""
            for j in range(6):
                item = self.data.tab1_pre[i * 6 + j]
                m += f"{j + 1}. {item[0]} 크리스탈 {item[1]}\n"
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

        embed.set_footer(text=self.data.time + " 기준")

        m = ""
        for i in range(len(self.data.tab2)):
            item = self.data.tab2[i]
            m += f"{i + 1}. {item[0]} 크리스탈 {item[1]}\n"
        if m == "":
            m = "현재 판매 상품이 없습니다"
        embed.add_field(name="현재 판매 상품", value=m)

        pre_num = int(len(self.data.tab2_pre) / 6)

        for i in range(pre_num):
            m = ""
            for j in range(6):
                item = self.data.tab2_pre[i * 6 + j]
                m += f"{j + 1}. {item[0]} 크리스탈 {item[1]}\n"
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

        embed.set_footer(text=self.data.time + " 기준")

        embed.add_field(name="💎골드 팔 때💎", value=self.data.golds["sell"])
        embed.add_field(name="💰골드 살 때💰", value=self.data.golds["buy"])

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="전각 시세 TOP 1-10", style=discord.ButtonStyle.grey, emoji="🥇")
    async def on_click_engraveds_1(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="전설 각인서 시세",
            url=self.data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.time + " 기준")

        engraveds = []
        for i in range(0, 10):
            engraveds.append("%02d. " % (i + 1) + str(self.data.engraveds[i]))

        embed.add_field(name="전각 시세 TOP 1-10", value="\n".join(engraveds))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="전각 시세 TOP 11-30", style=discord.ButtonStyle.grey, emoji="🥈")
    async def on_click_engraveds_2(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="전설 각인서 시세",
            url=self.data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.time + " 기준")

        engraveds = []
        for i in range(10, 30):
            engraveds.append("%02d. " % (i + 1) + str(self.data.engraveds[i]))

        embed.add_field(name="전각 시세 TOP 11-30", value="\n".join(engraveds))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="전각 시세 TOP 31-50", style=discord.ButtonStyle.grey, emoji="🥉")
    async def on_click_engraveds_3(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="전설 각인서 시세",
            url=self.data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.time + " 기준")

        engraveds = []
        for i in range(30, 50):
            engraveds.append("%02d. " % (i + 1) + str(self.data.engraveds[i]))

        embed.add_field(name="전각 시세 TOP 31-50", value="\n".join(engraveds))

        await self.message.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="전각 시세 TOP 51-", style=discord.ButtonStyle.grey, emoji="🎖")
    async def on_click_engraveds_4(self, interaction: discord.Interaction, button: discord.ui.button()):
        embed = discord.Embed(
            title="전설 각인서 시세",
            url=self.data.url,
            color=discord.Color.blue()
        )

        embed.set_footer(text=self.data.time + " 기준")

        engraveds = []
        for i in range(50, len(self.data.engraveds)):
            engraveds.append("%02d. " % (i + 1) + str(self.data.engraveds[i]))

        embed.add_field(name="전각 시세 TOP 51-", value="\n".join(engraveds))

        await self.message.edit(embed=embed)
        await interaction.response.defer()
