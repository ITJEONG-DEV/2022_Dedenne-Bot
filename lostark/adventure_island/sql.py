import os
import platform

import pymysql

from util import parse_json

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
key = None

if "Window" in platform.platform():
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dir_name = path + "\\json\\info.json"
    print(dir_name)
    key = parse_json(dir_name)
else:
    key = parse_json(path + "/data/info.json")

def connect():
    mysql = key["mysql"]
    return pymysql.connect(host=mysql["host"], user=mysql["user"], password=mysql["password"],
                           db=mysql["db"], charset='utf8')


con = connect()


# 기본 모험섬 정보가 DB에 있는지 확인
def check_adventure_island_available(name):
    global con
    if not con.begin():
        con = connect()

    cur = con.cursor()
    sql = f"SELECT COUNT(`ISLAND_NAME`) AS `COUNT` FROM `ISLAND_CONST` WHERE `ISLAND_NAME`='{name}';"
    cur.execute(sql)
    result = cur.fetchall()

    if result[0][0] == 0:
        return False
    else:
        return True


# 아이템 정보가 DB에 있는지 확인
def check_reward_item_available(name, grade):
    except_keyword_list = key["lostark"]["except_item"]

    for keyword in except_keyword_list:
        if keyword in name:
            return True

    global con
    if not con.begin():
        con = connect()

    cur = con.cursor()
    sql = f"SELECT COUNT(`REWARD_NAME`) AS `COUNT` FROM `REWARD_ITEM` WHERE `REWARD_NAME`='{name}' AND `ITEM_GRADE` = '{grade}';"
    cur.execute(sql)
    result = cur.fetchall()

    if result[0][0] == 0:
        return False
    else:
        return True


# 기본 리워드 정보가 DB에 있는지 확인
def check_reward_item_const_available(island, reward, grade):
    except_keyword_list = key["lostark"]["except_item"]

    for keyword in except_keyword_list:
        if keyword in reward:
            return True

    global con
    if not con.begin():
        con = connect()

    cur = con.cursor()
    sql = f"SELECT COUNT(`REWARD_NAME_`) AS `COUNT` FROM `ISLAND_REWARD_CONST` WHERE `REWARD_NAME_`='{reward}' AND `ISLAND_NAME_`='{island}' AND `ITEM_GRADE_`='{grade}';"
    cur.execute(sql)
    result = cur.fetchall()

    if result[0][0] == 0:
        return False
    else:
        return True


# 모험섬 스케쥴이 DB에 있는지 확인
def check_island_reward_schedule_available(date, time, island, reward, grade):
    except_keyword_list = key["lostark"]["except_item"]

    for keyword in except_keyword_list:
        if keyword in reward:
            return True

    global con
    if not con.begin():
        con = connect()

    cur = con.cursor()
    sql = f"SELECT COUNT(`REWARD_NAME`) AS `COUNT` FROM `ISLAND_REWARD_SCHEDULE` WHERE `REWARD_NAME`='{reward}' AND `ISLAND_NAME`='{island}' AND `APPEAR_DATE`='{date}' AND `PART_TIME`='{time}' AND `ITEM_GRADE`='{grade}';"
    cur.execute(sql)
    result = cur.fetchall()

    if result[0][0] == 0:
        return False
    else:
        return True


# 모험섬 보상 스케쥴이 DB에 있는지 확인
def check_island_schedule_available(date, time, name):
    global con
    if not con.begin():
        con = connect()

    cur = con.cursor()
    sql = f"SELECT COUNT(`ISLAND_NAME`) AS `COUNT` FROM `ISLAND_SCHEDULE` WHERE `ISLAND_NAME`='{name}' AND `APPEAR_DATE`='{date}' AND `PART_TIME`='{time}';"
    cur.execute(sql)
    result = cur.fetchall()

    if result[0][0] == 0:
        return False
    else:
        return True


# 기본 모험섬 정보를 DB에 추가
def add_adventure_island_const(name, url):
    global con
    if not con.begin():
        con = connect()

    try:
        cur = con.cursor()
        sql = f"INSERT INTO `ISLAND_CONST`(`ISLAND_NAME`, `ISLAND_ICON`) VALUES ('{name}', '{url}');"
        cur.execute(sql)
        con.commit()

    except Exception as e:
        print(e)


# 아이템 정보를 DB에 추가
def add_reward_item_const(name, url, grade):
    except_keyword_list = key["lostark"]["except_item"]

    for keyword in except_keyword_list:
        if keyword in name:
            return

    global con
    if not con.begin():
        con = connect()

    try:
        cur = con.cursor()
        sql = f"INSERT INTO `REWARD_ITEM`(`REWARD_NAME`, `REWARD_ICON`, `ITEM_GRADE`) VALUES ('{name}', '{url}', '{grade}');"
        cur.execute(sql)
        con.commit()

    except Exception as e:
        print(e)


# 기본 리워드 정보를 DB에 추가
def add_default_reward_item(island, reward, grade):
    except_keyword_list = key["lostark"]["except_item"]

    for keyword in except_keyword_list:
        if keyword in reward:
            return

    global con
    if not con.begin():
        con = connect()

    try:
        cur = con.cursor()
        sql = f"INSERT INTO `ISLAND_REWARD_CONST`(`ISLAND_NAME_`, `REWARD_NAME_`, `ITEM_GRADE_`) VALUES ('{island}', '{reward}', '{grade}');"
        cur.execute(sql)
        con.commit()

    except Exception as e:
        print(e)


# 모험섬 출연 정보를 DB에 추가
def add_adventure_island_schedule(name, date, time):
    global con
    if not con.begin():
        con = connect()
    try:
        cur = con.cursor()
        sql = f"INSERT INTO `ISLAND_SCHEDULE`(`APPEAR_DATE`, `PART_TIME`, `ISLAND_NAME`) VALUES ('{date}', '{time}', '{name}');"
        cur.execute(sql)
        con.commit()

    except Exception as e:
        print(e)


# 모험섬 보상 스케쥴을 DB에 추가
def add_island_reward_schedule(date, time, island, reward, grade):
    except_keyword_list = key["lostark"]["except_item"]

    for keyword in except_keyword_list:
        if keyword in reward:
            return

    global con
    if not con.begin():
        con = connect()

    try:
        cur = con.cursor()
        sql = f"INSERT INTO `ISLAND_REWARD_SCHEDULE`(`APPEAR_DATE`, `PART_TIME`, `ISLAND_NAME`, `REWARD_NAME`, `ITEM_GRADE`) VALUES ('{date}', '{time}', '{island}', '{reward}', '{grade}');"
        cur.execute(sql)
        con.commit()

    except Exception as e:
        print(e)


def get_adventure_island_reward_info(date, time):
    global con
    if not con.begin():
        con = connect()

    cur = con.cursor()

    # 해당하는 시간대의 모험섬 등장 정보 가져오기
    sql = f"SELECT * FROM `ISLAND_SCHEDULE` WHERE `APPEAR_DATE` = '{date}' AND `PART_TIME` = {time};"
    cur.execute(sql)
    result = cur.fetchall()

    island = [item[-1] for item in result]

    reward_dict = {}

    grade_rank = {
        "일반": 7,
        "고급": 6,
        "희귀": 5,
        "영웅": 4,
        "전설": 3,
        "유물": 2,
        "고대": 1,
        "에스더": 0
    }

    if len(result) > 0:
        for name in island:
            # 변동 보상 추가
            sql = f"SELECT `REWARD_NAME`, `ITEM_GRADE` FROM `ISLAND_REWARD_SCHEDULE` WHERE `APPEAR_DATE` = '{date}' AND `PART_TIME` = '{time}' AND `ISLAND_NAME` = '{name}';"
            cur.execute(sql)
            result = cur.fetchall()

            result = list(result)

            # 고정 보상 추가
            sql = f"SELECT `REWARD_NAME_`, `ITEM_GRADE_` FROM `ISLAND_REWARD_CONST` WHERE `ISLAND_NAME_` = '{name}';"
            cur.execute(sql)
            result2 = cur.fetchall()

            for item in result2:
                result.append(item)

            result = sorted(result, key=lambda x: grade_rank[x[1]])

            # 중복체크
            if result.count(('실링', '일반')) == 2:
                result.remove(('실링', '일반'))

            # 골드 섬
            if result.count(('골드', '일반')) > 0:
                item = result.pop(result.index(('골드', '일반')))
                result.insert(0, item)

            # 카드 섬
            elif result.count(('전설 ~ 고급 카드 팩', '전설')) > 0:
                item = result.pop(result.index(('전설 ~ 고급 카드 팩', '전설')))
                result.insert(0, item)

                item = result.pop(result.index(('영혼의 잎사귀', '고급')))
                result.insert(1, item)

            # 주화 섬
            elif result.count(('대양의 주화 상자', '영웅')) > 0:
                item = result.pop(result.index(('대양의 주화 상자', '영웅')))
                result.insert(0, item)
            elif result.count(('해적 주화', '일반')) > 0:
                item = result.pop(result.index(('해적 주화', '일반')))
                result.insert(0, item)

            # 실링 섬
            elif result.count(('실링', '일반')) > 0:
                item = result.pop(result.index(('실링', '일반')))
                result.insert(0, item)

            reward_dict[name] = result

        return list(reward_dict.items())

    else:
        return None


if __name__ == "__main__":
    print("hi")
    # print(get_advendure_island_info(date="2023-03-11", time="0"))
