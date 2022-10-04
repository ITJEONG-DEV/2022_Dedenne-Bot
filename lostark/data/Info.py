class Info:
    def __init__(self):
        self.__member_no = ""
        self.__pc_id = ""
        self.__world_no = ""

    @property
    def member_no(self):
        return self.__member_no

    @member_no.setter
    def member_no(self, value):
        self.__member_no = value

    @property
    def pc_id(self):
        return self.__pc_id

    @pc_id.setter
    def pc_id(self, value):
        self.__pc_id = value

    @property
    def world_no(self):
        return self.__world_no

    @world_no.setter
    def world_no(self, value):
        self.__world_no = value

