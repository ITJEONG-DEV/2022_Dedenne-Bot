class Work:
    def __init__(self, command, contents):
        self.__command = command
        self.__contents = contents

    @property
    def command(self):
        return self.__command

    @property
    def contents(self):
        return self.__contents
