class Video:
    def __init__(self, video_id: str, title: str, thumbnail: str):
        self.__id = video_id
        self.__title = title
        self.__thumbnail = thumbnail
        self.__error = None

    @property
    def url(self):
        return "https://www.youtube.com/watch?v=" + self.__id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def thumbnail(self):
        return self.__thumbnail

    @thumbnail.setter
    def thumbnail(self, value):
        self.__thumbnail = value

    @property
    def error(self):
        return self.__error

    @error.setter
    def error(self, value):
        self.__error = value
