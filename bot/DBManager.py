import pymysql

from util import parse_json


class DBManager:
    def __init__(self):
        self.data = parse_json("json/info.json")["mysql"]

        self.con = None
        self.cur = None

    def connect(self):
        if self.con is None:
            self.con = pymysql.connect(
                host='localhost',
                user=self.data["user"],
                password=self.data["password"],
                db=self.data["db"],
                charset="utf8"
            )

    def get_adventure_island_information(self, key):
        cur = self.con.cursor()
        sql = f"SELECT `ISLAND`, `REWARD` FROM ADVENTURE_ISLAND WHERE `ID` = {key};"
        cur.execute(sql)
        rows = cur.fetchall()

        return rows[0]

    def check_duplicate(self, character_name):
        self.connect()

        query = f"SELECT _username, _charactername FROM member WHERE _charactername = '{character_name}';"
        self.cur.execute(query)

        rows = self.cur.fetchall()

        if len(rows) == 0:
            return False
        else:
            return True

    def add(self, user_name, character_name):
        self.connect()

        # 중복 검사
        if self.check_duplicate(character_name):
            query = f"INSERT INTO member (_username, _charactername, _time) VALUES ('{user_name}', '{character_name}', NOW());"
            self.cur.execute(query)
            self.con.commit()

            return "added_member_success"
        else:
            return "added_member_failed"

    def remove_character(self, character_name):
        self.connect()

        query = f"DELETE FROM member WHERE _charactername = '{character_name}';"
        self.cur.execute(query)
        self.con.commit()

    def show(self):
        self.connect()

        query = f"SELECT _username, _charactername FROM member;"
        self.cur.execute(query)

        rows = self.cur.fetchall()

        return rows

    def close(self):
        if self.con is not None:
            self.con.close()

        self.cur = None
        self.con = None


if __name__ == "__main__":
    db_manager = DBManager()
    db_manager.connect()
    db_manager.remove_character("데덴네귀여워")
    db_manager.show()
