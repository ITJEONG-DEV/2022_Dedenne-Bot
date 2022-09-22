class Task:
    def __init__(self, guild_id, channel_id, user_id, search_result):
        self.__guild_id = guild_id
        self.__chanel_id = channel_id
        self.__user_id = user_id
        self.__search_result = search_result

    @property
    def key(self):
        return str(self.__guild_id) + str(self.__chanel_id) + "``" + str(self.__user_id)

    @property
    def guild_id(self):
        return self.__guild_id

    @property
    def chanel_id(self):
        return self.__chanel_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def search_result(self):
        return self.__search_result
