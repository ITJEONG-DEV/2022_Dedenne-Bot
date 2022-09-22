import asyncio
from enum import Enum

from bot import *
from data import *
from util import parse_json

from youtube.youtube import YoutubeHandler, YTDLSource


class PlayingState(Enum):
    NONE = 0,
    READY = 1,
    PLAYING = 2,
    PAUSE = 3,
    STOP = 4
    END = 5


class BotWorker:
    def __init__(self, bot):
        self.bot = bot

        # task 임시 저장 queue
        self.task_queue = Queue()

        # 재생목록
        self.music_queue = Queue()

        self.handle_list = {
            # general_command
            "help": self.__help,
            "introduce": self.__introduce,
            "join": self.__join,
            "leave": self.__leave,
            "search": self.__search,
            "select": self.__select,
            "add": self.__add,
            "queue": self.__queue,
            "play": self.__play,
            "pause": self.__pause,
            "resume": self.__resume,
            "stop": self.__stop,
            "skip": self.__skip,
            "add_queue": self.__add_queue,
            "shuffle": self.__shuffle
        }

        self.youtube_handler = YoutubeHandler(parse_json("json/info.json")["youtube"]["api_key"])

        self.voice_channel = None
        self.voice_client = None

        self.playing_state = PlayingState.NONE
        print("Start BotWorker")

    async def handle(self, item: Work):
        await self.handle_list[item.command](item)

    async def __help(self, item: Work):
        await self.bot.send_message(
            channel=item.contents["channel"],
            contents="help"
        )

    async def __introduce(self, item: Work):
        await self.bot.send_message(
            channel=item.contents["channel"],
            contents="introduce"
        )

    async def __join(self, item: Work):
        guild = item.contents["guild"]
        channel = item.contents["channel"]
        user = item.contents["author"]

        if not user.voice:
            await self.bot.send_specify_message(channel, "join_error", user.name)
            return False

        self.voice_channel = user.voice.channel

        if self.voice_client is None:
            self.voice_client = guild.voice_client

        try:
            await self.voice_channel.connect()
            self.playing_state = PlayingState.READY

            await self.bot.send_specify_message(channel, "join_message", self.voice_channel.name)

        except Exception as e:
            print("Error when joining voice channel: " + e)
            return False

        return True

    async def __leave(self, item: Work):
        guild = item.contents["guild"]
        channel = item.contents["channel"]

        if self.voice_channel is None:
            await self.bot.send_specify_message(channel, "not_join_error", self.bot.user.name)
            return

        if self.voice_client is None:
            self.voice_client = guild.voice_client

        if self.voice_client.is_connected():
            self.playing_state = PlayingState.NONE

            if self.voice_client.is_playing():
                self.voice_client.stop()

            await self.voice_client.disconnect()

            await self.bot.send_specify_message(channel, "leave_message", self.voice_channel.name)

            self.voice_channel = None
            self.voice_client = None

        else:
            await self.bot.send_specify_message(channel, "not_join_error", self.bot.user.name)

    def __get_search_result_string(self, search_result):
        msg = "*🔎검색결과🔎*\n"

        for i in range(len(search_result)):
            item = search_result[i]

            msg += "  " + str(i + 1) + ". " + item.title + "\n"

        msg += "'선택 n'으로 입력>>"
        return msg

    async def __search(self, item: Work):
        guild_id = item.contents["guild"].id
        channel = item.contents["channel"]
        user_id = item.contents["author"].id
        keyword = " ".join(item.contents["message"].split()[1:])

        search_result = self.youtube_handler.get_search_result(keyword)

        await self.bot.send_message(
            channel=channel,
            contents=self.__get_search_result_string(search_result)
        )

        task = Task(
            guild_id=guild_id,
            channel_id=channel.id,
            user_id=user_id,
            search_result=search_result
        )

        for i in range(self.task_queue.length()):
            if task.key == self.task_queue.get(i).key:
                self.task_queue.remove_at(i)
                break

        self.task_queue.enqueue(task)

    async def __select(self, item: Work):
        task = self.task_queue.dequeue()

        if task is not None:
            search_result = task.search_result

            nums = item.contents["message"].split()[1:]

            for num in nums:
                num = int(num)

                if 0 < num <= len(search_result):
                    target = search_result[num - 1]

                    contents = item.contents
                    contents["video"] = target

                    work = Work(
                        command="add_queue",
                        contents=contents
                    )

                    await self.__add_queue(work)

    async def __add(self, item: Work):
        channel = item.contents["channel"]
        url = item.contents["message"].split()[1]

        video = self.youtube_handler.get_video_info(url)

        if video.error is not None:
            await self.bot.send_specify_message(channel, "invalid_link_error")
            return

        contents = item.contents
        contents["video"] = video

        work = Work(
            command="add_queue",
            contents=contents
        )

        await self.__add_queue(work)

    async def __queue(self, item: Work):
        channel = item.contents["channel"]

        msg = "*🎵현재 재생목록🎵*\n"
        for i in range(self.music_queue.length()):
            item = self.music_queue.get(i)

            msg += "{}. {}\n".format((i + 1), item.title)

        await self.bot.send_message(channel, msg)

    def __play_ended(self, error):
        if error:
            print("__play_ended gets error message: " + str(error))
            return

        if self.playing_state == PlayingState.STOP or self.playing_state == PlayingState.NONE:
            return

        self.playing_state = PlayingState.END

        if self.music_queue.length() > 0:
            fut = asyncio.run_coroutine_threadsafe(self.__play(), self.bot.loop)
            try:
                fut.result()
            except Exception as e:
                print("__play_ended gets error message 2: " + e)

    async def __try_play(self, item: Work):
        if self.voice_channel is None:
            result = await self.__join(item)

            if not result:
                return

        self.guild = item.contents["guild"]
        self.channel = item.contents["channel"]

        if self.voice_client is None:
            self.voice_client = self.guild.voice_client

        if not self.voice_client.is_playing():
            await self.__play()

    async def __play(self):
        # if self.voice_channel is None:
        #     await self.__join(item)

        video = self.music_queue.dequeue()

        if video is None:
            await self.bot.send_specify_message(self.channel, "empty_queue_error")
            return

        try:
            # self.voice_client = self.guild.voice_client

            player = await YTDLSource.from_url(video.url, loop=False, stream=True)

            # self.voice_client.play(player, after=lambda e:asyncio.new_event_loop()(self.__play_ended()))
            # self.voice_client.play(player, after=lambda e: self.loop.run_until_complete(self.future))
            self.voice_client.play(player, after=lambda e: self.__play_ended(e))

            self.playing_state = PlayingState.PLAYING

            await self.bot.send_specify_message(self.channel, "play_message", player.title)
            # await self.bot.send_message(self.channel, '{}'.format(video.thumbnail))

        except Exception as e:
            print("Error when try playing: " + str(e))
            await self.bot.send_specify_message(self.channel, "playing_error", str(e))
            self.playing_state = PlayingState.READY

    async def __pause(self, item: Work):
        channel = item.contents["channel"]

        if self.voice_channel is None or self.voice_client is None:
            await self.bot.send_specify_message(channel, "not_join_error", self.bot.user.name)
            return

        if self.voice_client.is_playing():
            self.voice_client.pause()
            self.playing_state = PlayingState.PAUSE

            await self.bot.send_specify_message(channel, "pause_message")

        else:
            await self.bot.send_specify_message(channel, "not_playing_error", self.bot.user.name)

    async def __resume(self, item: Work):
        channel = item.contents["channel"]

        if self.voice_channel is None or self.voice_client is None:
            await self.bot.send_specify_message(channel, "not_join_error", self.bot.user.name)
            return

        if self.voice_client.is_paused():
            self.voice_client.resume()
            self.playing_state = PlayingState.PLAYING

            await self.bot.send_specify_message(channel, "resume_message")

        else:
            await self.bot.send_specify_message(channel, "not_playing_error", self.bot.user.name)

    async def __stop(self, item: Work):
        channel = item.contents["channel"]

        if self.voice_channel is None or self.voice_client is None:
            await self.bot.send_specify_message(channel, "not_join_error", self.bot.user.name)
            return

        if self.voice_client.is_playing():
            self.voice_client.stop()

            self.playing_state = PlayingState.STOP

            await self.bot.send_specify_message(channel, "stop_message")

        else:
            await self.bot.send_specify_message(channel, "isnt_playing_error", self.bot.user.name)

    async def __skip(self, item: Work):
        channel = item.contents["channel"]
        guild = item.contents["guild"]

        if self.voice_channel is None or self.voice_client is None:
            await self.bot.send_specify_message(channel, "not_join_error", self.bot.user.name)
            return

        if self.voice_client.is_playing():
            if self.music_queue.length() == 0:
                self.playing_state = PlayingState.STOP

            self.voice_client.stop()

            await self.bot.send_specify_message(channel, "skip_message")

        else:
            await self.bot.send_specify_message(channel, "isnt_playing_error", self.bot.user.name)
            return

    async def __add_queue(self, item: Work):
        channel = item.contents["channel"]

        video = item.contents["video"]

        self.music_queue.enqueue(video)

        await self.bot.send_specify_message(channel, "add_queue_message", video.title)

        await self.__try_play(item)

    async def __shuffle(self, item: Work):
        channel = item.contents["channel"]

        self.music_queue.shuffle()
        await self.bot.send_specify_message(channel, "shuffle_message")
        await self.__queue(item)
