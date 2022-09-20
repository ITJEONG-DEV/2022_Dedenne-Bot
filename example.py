import json

import discord


def parse_token(url="info.json"):
    with open(url, "r", encoding="UTF-8") as json_txt:
        json_contents = json.load(json_txt)

        return json_contents["discord"]["token"]


def parse_words(url="words.json"):
    with open(url, "r", encoding="UTF-8") as json_txt:
        json_contents = json.load(json_txt)

        return json_contents["words"]


class DedenneBot(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)
        self.words = parse_words()

    async def on_message(self, message):
        # '봇' 또는 'bot' 이 포함된 채널에만 반응
        if "봇" not in message.channel.name and "bot" not in message.channel.name:
            return

        # 본인이 보낸 메시지에는 반응하지 않음
        if message.author == self.user:
            return

        result = self.get_return_words(message.content)

        if result is not None:
            commands = result.split("_")

            command = commands[0]
            content = commands[1]

            # 단순 출력 커맨드
            if command == "m":
                await message.channel.send(content + " " + message.author.name)

            elif command == "c":
                # command 처리
                print(content)

        else:
            await message.channel.send(message.content)

    def get_return_words(self, message):
        if self.words is not None:
            for return_word, words in self.words.items():
                for word in words:
                    if word in message:
                        return return_word

        return None


my_intents = discord.Intents.default()
my_intents.message_content = True
my_intents.typing = False
my_intents.presences = False

client = DedenneBot(intents=my_intents)
client.run(token=parse_token())  # 토큰
