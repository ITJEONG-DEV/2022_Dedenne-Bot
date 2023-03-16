import discord

from bot.DedenneBotv2 import DedenneBot
from util import parse_json

import os
path = os.path.dirname(os.path.abspath(__file__))

my_intents = discord.Intents.default()
my_intents.message_content = True
my_intents.typing = False
my_intents.presences = False
my_intents.members = True

client = DedenneBot(intents=my_intents)
client.run(token=parse_json("./json/info.json")["discord"]["token"])  # 토큰
