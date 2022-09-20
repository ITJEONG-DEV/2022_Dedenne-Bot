import json

import discord


def parse_token(url="info.json"):
    with open(url, "r", encoding="UTF-8") as json_txt:
        json_contents = json.load(json_txt)

        return json_contents["discord"]["token"]


def parse_words(url="command_collection.json"):
    with open(url, "r", encoding="UTF-8") as json_txt:
        json_contents = json.load(json_txt)

        return json_contents


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

        return_words = self.get_return_words(message.content)

        if return_words is not None:
            words = return_words.split("_")

            command = words[0]
            content = words[1]

            # 단순 출력 커맨드
            if command == "m":
                await message.channel.send(content + " " + message.author.name)

            # 명령어
            elif command == "c":
                command_contents = self.get_command_contents(content)

                if content == "help":
                    await message.channel.send(command_contents["text"])

                else:
                    await message.channel.send("%s 기능 미구현" % content)

        else:
            await message.channel.send(message.content)

    def get_return_words(self, message):
        for item in self.words["words"]:
            for word in item["trigger_words"]:
                if word in message:
                    return item["return_word"]

        return None

    def get_command_contents(self, command):
        for item in self.words["commands"]:
            if item["command"] == command:
                return item

        return None


my_intents = discord.Intents.default()
my_intents.message_content = True
my_intents.typing = False
my_intents.presences = False

client = DedenneBot(intents=my_intents)
client.run(token=parse_token())  # 토큰
