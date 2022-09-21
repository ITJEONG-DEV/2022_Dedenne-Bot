from enum import Enum
import threading
import time

import discord
from discord.ext.commands import bot

from youtube.youtube import YoutubeHandler, YTDLSource
from util import *


class State(Enum):
    DEFAULT = 0,
    READY = 1,
    PLAYING = 2,
    PAUSE = 3,
    STOP = 4


class DedenneBot(discord.Client):

    def set_state(self, state):
        self.state = state

    async def on_ready(self):
        self.__words = parse_json("data/command_collection.json")

        self.youtube_handler = YoutubeHandler(parse_json("data/info.json")["youtube"]["api_key"])

        self.current_thread = None

        self.task = {}
        self.__queue = []

        self.voice_channel = None
        self.voice_client = None

        self.state = State.DEFAULT

        print('Logged on as', self.user)
        self.set_state(State.READY)

    async def on_message(self, message):
        if self.state == State.DEFAULT:
            return

        # '봇' 또는 'bot' 이 포함된 채널에만 반응
        if "봇" not in message.channel.name and "bot" not in message.channel.name:
            return

        # 본인이 보낸 메시지에는 반응하지 않음
        if message.author == self.user:
            return

        return_words = self.__get_return_words(message.content)

        if return_words is not None:
            words = return_words.split("_")

            command = words[0]
            content = words[1]

            # 단순 출력 커맨드
            if command == "m":
                await DedenneBot.send_message(message.channel, content + " " + message.author.name)

            # 명령어
            elif command == "c":
                command_contents = self.__get_command_contents(content)

                if content == "!help":
                    await DedenneBot.send_message(message.channel, command_contents["text"])

                elif content == "!introduce":
                    await DedenneBot.send_message(message.channel, command_contents["text"])

                elif content == "!search":
                    keyword = " ".join(message.content.split()[1:])
                    await self.search(message.channel, message.author.id, keyword)

                elif content == "!select":
                    await self.select(message.guild, message.channel, message.author, message.content)

                elif content == "!add":
                    url = message.content.split()[1]
                    await self.add(message.guild, message.channel, message.author, url)

                else:
                    await DedenneBot.send_message(message.channel, "%s 기능 미구현" % content)

        else:
            try:
                await DedenneBot.send_message(message.channel, message.content)
            except Exception as e:
                print("Error occurred: ", e)

    @staticmethod
    async def send_message(channel, contents):
        await channel.send(contents)

    async def search(self, channel, user_id, keyword):
        search_result = self.youtube_handler.get_search_result(keyword)
        await channel.send(self.__get_search_result_string(search_result))

        self.__add_task(
            channel_id=channel.id,
            user_id=user_id,
            search_result=search_result
        )

    async def select(self, guild, channel, user, content):
        search_result = self.__get_task(
            channel_id=channel.id,
            user_id=user.id
        )

        if search_result is not None:
            nums = content.split()[1:]

            for num in nums:
                num = int(num)
                if 0 < num <= len(search_result):
                    target = search_result[num - 1]

                    self.__enqueue(target)
                    await DedenneBot.send_message(channel, "'{}'가 queue에 추가되었어요".format(target["title"]))

                    if self.state == State.READY or self.state == State.PAUSE or self.state == State.STOP:
                        await self.play(guild, channel, user)
                    # await channel.send(target["url"])

    async def add(self, guild, channel, user, url):
        target = self.youtube_handler.get_video_info(url)

        if "error" in target.keys():
            await DedenneBot.send_message(channel, "잘못된 링크에요")
            return

        self.__enqueue(target)

        await DedenneBot.send_message(channel, "'{}'가 queue에 추가되었어요".format(target["title"]))

        if self.state == State.READY or self.state == State.PAUSE or self.state == State.STOP:
            await self.play(guild, channel, user)

    async def join(self, channel, user):
        if not user.voice:
            await DedenneBot.send_message(channel, "{}님, 먼저 음성 채널에 참여해 주세요.".format(user.name))
            return

        self.voice_channel = user.voice.channel

        await self.voice_channel.connect()

    async def leave(self, ctx):
        if self.voice_channel is None:
            await ctx.send("{}은 음성 채널에 참여하고 있지 않아요".format(self.user.name))
            return

        if self.voice_channel.is_connected():
            await self.voice_channel.disconnect()

            self.voice_channel = None
            self.voice_client = None

        else:
            await ctx.send("{}은 음성 채널에 참여하고 있지 않아요".format(self.user.name))
            return

    async def play(self, guild, channel, user):
        if self.voice_channel is None:
            await self.join(channel, user)

        target = self.__dequeue()

        if target is None:
            await DedenneBot.send_message(channel, "재생할 노래가 없어요")
            return

        url = "https://www.youtube.com/watch?v=" + target["id"]

        try:
            self.voice_client = guild.voice_client

            player = await YTDLSource.from_url(url=url, loop=False, stream=True)

            self.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

            await DedenneBot.send_message(channel, '**현재 재생 중인 영상:** {}'.format(player.title))

            self.current_thread = threading.Thread(target=self.__check_playing_status, args=[guild, channel, user])
            self.current_thread.daemon = True
            self.current_thread.start()

            self.set_state(State.PLAYING)

        except Exception as e:
            await DedenneBot.send_message(channel, "재생 시도 중 오류 발생! {}".format(e))

    def __check_playing_status(self, guild, channel, user):
        while True:
            time.sleep(1)

            if self.state == State.PLAYING or self.state == State.PAUSE:
                continue

            if not self.voice_client.is_playing():
                break

        if self.__get_queue_length() > 0:
            self.play(guild, channel, user)

    async def pause(self, ctx):
        if self.voice_channel is None:
            await ctx.send("{}은 음성 채널에 참여하고 있지 않아요".format(self.user.name))
            return

        if self.voice_client is None:
            self.voice_client = ctx.message.guild.voice_client

        if self.voice_client.is_playing():
            await self.voice_client.pause()
            self.set_state(State.PAUSE)
        else:
            await ctx.send("{}이 현재 재생 중인 노래가 없어요".format(self.user.name))

    async def resume(self, ctx):
        if self.voice_channel is None:
            await ctx.send("{}은 음성 채널에 참여하고 있지 않아요".format(self.user.name))
            return

        if self.voice_client is None:
            self.voice_client = ctx.message.guild.voice_client

        if self.voice_client.is_paused():
            await self.voice_client.resume()
            self.set_state(State.PLAYING)

        else:
            await ctx.send("{}이 이전에 재생 중이던 노래가 없어요".format(self.user.name))

    async def stop(self, ctx):
        if self.voice_channel is None:
            await ctx.send("{}은 음성 채널에 참여하고 있지 않아요".format(self.user.name))
            return

        if self.voice_client is None:
            self.voice_client = ctx.message.guild.voice_client

        if self.voice_client.is_playing():
            await self.voice_client.stop()
            self.set_state(State.STOP)
        else:
            await ctx.send("{}이 이전에 재생 중이던 노래가 없어요".format(self.user.name))

    def __add_task(self, channel_id, user_id, search_result):
        key = str(channel_id) + "``" + str(user_id)

        self.task[key] = search_result

    def __get_task(self, channel_id, user_id):
        key = str(channel_id) + "``" + str(user_id)

        if key in self.task.keys():
            return self.task.pop(key)
        else:
            return None

    def __enqueue(self, content):
        self.__queue.append(content)

    def __dequeue(self):
        if len(self.__queue) == 0:
            return None
        else:
            return self.__queue.pop(0)

    def __get_queue_length(self):
        return len(self.__queue)

    def __get_search_result_string(self, search_result):
        msg = "[검색결과]\n"

        for i in range(len(search_result)):
            item = search_result[i]

            # url = "https://www.youtube.com/watch?v=" + item["id"]
            msg += "  " + str(i + 1) + ". " + item["title"] + "\n"

        msg += "**선택 n으로 입력>>**"
        return msg

    def __get_return_words(self, message):
        for item in self.__words["words"]:
            for word in item["trigger_words"]:
                if word in message:
                    return item["return_word"]

        return None

    def __get_command_contents(self, command):
        for item in self.__words["commands"]:
            if item["command"] == command:
                return item

        return None
