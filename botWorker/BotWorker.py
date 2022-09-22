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
            "stop": self.__stop,
            "skip": self.__skip,
            "add_queue": self.__add_queue,
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
        channel = item.contents["channel"]
        user = item.contents["author"]

        if not user.voice:
            await self.bot.send_message(
                channel=channel,
                contents="{}님, 먼저 음성 채널에 참여해 주세요.".format(user.name)
            )
            return

        self.voice_channel = user.voice.channel

        try:
            await self.voice_channel.connect()
            self.playing_state = PlayingState.READY
        except Exception as e:
            print("Error when joining voice channel: " + e)

    async def __leave(self, item: Work):
        channel = item.contents["channel"]

        if self.voice_channel is None:
            await self.bot.send_message(
                channel=channel,
                contents="{}은 음성 채널에 참여하고 있지 않아요".format(DedenneBot.user.name)
            )
            return

        if self.voice_client.is_connected():
            await self.voice_client.disconnect()

            self.voice_channel = None
            self.voice_client = None

            self.playing_state = PlayingState.NONE
        else:
            await self.bot.send_message(
                channel=channel,
                contents="{}은 음성 채널에 참여하고 있지 않아요".format(self.bot.user.name)
            )

    def __get_search_result_string(self, search_result):
        msg = "[검색결과]\n"

        for i in range(len(search_result)):
            item = search_result[i]

            msg += "  " + str(i + 1) + ". " + item.title + "\n"

        msg += "**선택 n으로 입력>>**"
        return msg

    async def __search(self, item: Work):
        channel = item.contents["channel"]
        user_id = item.contents["author"].id
        keyword = " ".join(item.contents["message"].split()[1:])

        search_result = self.youtube_handler.get_search_result(keyword)

        await self.bot.send_message(
            channel=channel,
            contents=self.__get_search_result_string(search_result)
        )

        task = Task(
            channel_id=channel.id,
            user_id=user_id,
            search_result=search_result
        )

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
            await self.bot.send_message(
                channel=channel,
                contents="잘못된 링크에요"
            )
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

        msg = "재생목록\n"
        for i in range(self.music_queue.length()):
            item = self.music_queue.get(i)

            msg += "{}. {}\n".format((i + 1), item.title)

        await self.bot.send_message(channel, msg)

    def __play_ended(self, error):
            self.playing_state = PlayingState.END

            if self.music_queue.length() > 0:
                fut = asyncio.run_coroutine_threadsafe(self.__play(), self.bot.loop)
                try:
                    fut.result()
                except Exception as e:
                    print(e)


    async def __try_play(self, item: Work):
        if self.voice_channel is None:
            await self.__join(item)

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
            await self.bot.send_message(self.channel, "재생할 노래가 없어요")
            return

        try:
            # self.voice_client = self.guild.voice_client

            player = await YTDLSource.from_url(video.url, loop=False, stream=True)

            # self.voice_client.play(player, after=lambda e:asyncio.new_event_loop()(self.__play_ended()))
            # self.voice_client.play(player, after=lambda e: self.loop.run_until_complete(self.future))
            self.voice_client.play(player, after=lambda e: self.__play_ended(e))

            self.playing_state = PlayingState.PLAYING

            await self.bot.send_message(self.channel, '**현재 재생 중인 영상: {}**'.format(player.title))
            await self.bot.send_message(self.channel, '{}'.format(video.thumbnail))

        except Exception as e:
            print("Error when try playing: " + str(e))
            await self.bot.send_message(self.channel, "재생 시도 중 오류 발생! {}".format(e))
            self.playing_state = PlayingState.READY

    async def __pause(self, item: Work):
        channel = item.contents["channel"]

        if self.voice_channel is None or self.voice_client is None:
            await self.bot.send_message(channel, "{}은 음성 채널에 참여하고 있지 않아요".format(self.bot.user.name))
            return

        if self.voice_client.is_playing():
            await self.voice_client.pause()
            self.playing_state = PlayingState.PAUSE
        else:
            await self.bot.send_message(channel, "{}이 현재 재생 중인 노래가 없어요".format(self.bot.user.name))

    async def __stop(self, item: Work):
        channel = item.contents["channel"]

        if self.voice_channel is None or self.voice_client is None:
            await self.bot.send_message(channel, "{}은 음성 채널에 참여하고 있지 않아요".format(self.bot.user.name))
            return

        if self.voice_client.is_playing():
            await self.voice_client.stop()
            self.playing_state = PlayingState.STOP
        else:
            await self.bot.send_message(channel, "{}이 이전에 재생 중이던 노래가 없어요".format(self.bot.user.name))

    async def __skip(self, item: Work):
        channel = item.contents["channel"]

        if self.voice_channel is None or self.voice_client is None:
            await self.bot.send_message(channel, "{}은 음성 채널에 참여하고 있지 않아요".format(self.bot.user.name))
            return

        if self.voice_client.is_playing():
            await self.voice_client.stop()

            video = self.music_queue.dequeue()

            if video is None:
                self.playing_state = PlayingState.STOP

            else:
                player = await YTDLSource.from_url(video.url, loop=False, stream=True)

                self.voice_client.play(player, after=lambda e: self.__play_ended())

                self.playing_state = PlayingState.PLAYING
        else:
            await self.bot.send_message(channel, "{}이 이전에 재생 중이던 노래가 없어요".format(self.bot.user.name))
            return

        await self.bot.send_message(channel, "노래를 스킵합니다".format(self.bot.user.name))

    async def __add_queue(self, item: Work):
        channel = item.contents["channel"]

        video = item.contents["video"]

        self.music_queue.enqueue(video)

        await self.bot.send_message(channel, "'{}'가 재생목록에 추가되었어요".format(video.title))

        await self.__try_play(item)
