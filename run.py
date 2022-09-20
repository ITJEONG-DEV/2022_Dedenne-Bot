import discord

from DedenneBot import DedenneBot
from util import parse_json


my_intents = discord.Intents.default()
my_intents.message_content = True
my_intents.typing = False
my_intents.presences = False

client = DedenneBot(intents=my_intents)
client.run(token=parse_json("./data/info.json")["discord"]["token"])  # 토큰
