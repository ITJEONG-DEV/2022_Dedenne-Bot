import datetime
from PIL import Image, ImageDraw, ImageFont

from sql import *

import os
import datetime
import requests

path = os.path.join(os.path.dirname(os.path.abspath(__file__)))

def get_adventure_island_info(authorization):
    request_url = "https://developer-lostark.game.onstove.com/gamecontents/calendar"

    response = requests.get(request_url, headers={'accept': 'application/json', 'authorization': authorization})

    adventure_island_list = []

    for item in response.json():
        if item["CategoryName"] == "모험 섬":
            adventure_island_list.append(item)

    return adventure_island_list


def parse_adventure_island(authorization):
    item_list = get_adventure_island_info(authorization)

    for item in item_list:
        # 기본 모험섬 정보를 체크한다
        if not check_adventure_island_available(name=item["ContentsName"]):
            # 기본 모험섬 정보 추가
            add_adventure_island_const(name=item["ContentsName"], url=item["ContentsIcon"])

        # 모험섬 출연 시간 확인(평일/주말-오전/주말-오후 등)
        start_time = []
        for time in item["StartTimes"]:
            date = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")

            # weekend
            if date.weekday() >= 5:
                if date.hour <= 18:
                    start_time.append((date.strftime("%Y-%m-%d"), 0))
                else:
                    start_time.append((date.strftime("%Y-%m-%d"), 1))
            else:
                start_time.append((date.strftime("%Y-%m-%d"), 0))

        start_time = set(start_time)

        # 섬 출연 정보를 DB에 추가한다
        for time in start_time:
            if not check_island_schedule_available(
                    name=item["ContentsName"],
                    date=time[0],
                    time=time[1]
            ):
                add_adventure_island_schedule(
                    name=item["ContentsName"],
                    date=time[0],
                    time=time[1]
                )

        # 모험섬 보상을 체크한다
        for reward in item["RewardItems"]:

            # 아이템 확인
            if not check_reward_item_available(
                    name=reward["Name"],
                    grade=reward["Grade"]
            ):
                # 아이템 정보 추가
                add_reward_item_const(
                    name=reward["Name"],
                    url=reward["Icon"],
                    grade=reward["Grade"]
                )

            # 기본 보상인지 확인한다
            if reward["StartTimes"] is None:
                if not check_reward_item_const_available(
                        island=item["ContentsName"],
                        reward=reward["Name"],
                        grade=reward["Grade"]
                ):
                    # 기본 보상 정보 추가
                    add_default_reward_item(
                        island=item["ContentsName"],
                        reward=reward["Name"],
                        grade=reward["Grade"]
                    )

            else:
                reward_time = []
                for time in reward["StartTimes"]:
                    date = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")

                    # weekend
                    if date.weekday() >= 5:
                        if date.hour <= 18:
                            reward_time.append((date.strftime("%Y-%m-%d"), 0))
                        else:
                            reward_time.append((date.strftime("%Y-%m-%d"), 1))
                    else:
                        reward_time.append((date.strftime("%Y-%m-%d"), 0))

                reward_time = set(reward_time)

                # 모험섬 보상 스케쥴 존재 여부 확인 후, 모험섬 보상 스케쥴 추가
                for time in reward_time:
                    if not check_island_reward_schedule_available(
                            date=time[0],
                            time=time[1],
                            island=item["ContentsName"],
                            reward=reward["Name"],
                            grade=reward["Grade"]
                    ):
                        add_island_reward_schedule(
                            date=time[0],
                            time=time[1],
                            island=item["ContentsName"],
                            reward=reward["Name"],
                            grade=reward["Grade"]
                        )

    print("[Done] parsing adventure island information")


# 파일이 있는지 확인하고, 없다면 다운로드 받아서 반환
def get_image(name: str):
    name = name.replace(":", "")

    if not os.path.isfile(f'{path}/data/resource/{name}.png'):
        print("download request")

    return Image.open(f'{path}/data/resource/{name}.png').convert("RGBA")


# 일반 고급 희귀 영웅 전설 유물 고대 에스더
# 회색 초록 파랑 보라 금색 빨강 하양 하늘색
grade_color = {
    "일반": (78, 80, 77),
    "고급": (56, 74, 34),
    "희귀": (15, 49, 74),
    "영웅": (65, 28, 79),
    "전설": (115, 78, 25),
    "유물": (164, 69, 15),
    "고대": (248, 228, 178),
    "에스더": (122, 245, 247)
}


def get_item_color(grade: str):
    if grade in grade_color.keys():
        return grade_color[grade]
    else:
        return grade_color["일반"]


window_size = (1024, 512)
icon_size = (64, 64)


title_font = ImageFont.truetype(f"{path}/data/resource/NanumBarunGothicBold.ttf", size=40)
time_font = ImageFont.truetype(f"{path}/data/resource/NanumBarunGothic.ttf", size=32)
island_font = ImageFont.truetype(f"{path}/data/resource/NanumBarunGothic.ttf", size=28)
item_color = (50, 50, 50)

background_color = (0, 0, 0)
title_back_color = (32, 32, 32)

# background_color = (32, 32, 32)
# title_back_color = (0, 0, 0)

font_color = (255, 255, 255)
title_color = (255, 210, 40)
icon_gap = 4  # 아이콘 사이의 공백
content_gap = 32  # 컨텐츠 사이의 공백
max_reward_num = 8
margin = 4


def make_rewards_box(rewards: [], grades: []):
    width, height = icon_size[0] * len(rewards) + icon_gap * (len(rewards) - 1), icon_size[1]
    reward_box_size = (width, height)
    reward_box = Image.new('RGBA', reward_box_size, background_color)

    for i in range(len(rewards)):
        reward = rewards[i]
        grade = grades[i]

        reward_back = Image.new('RGBA', icon_size, get_item_color(grade))

        reward_image = get_image(reward)
        reward_image = reward_image.resize(icon_size)

        start_x, start_y = (icon_size[0] + icon_gap) * i, 0
        reward_image = Image.alpha_composite(reward_back, reward_image)
        reward_box.paste(reward_image, (start_x, start_y), reward_image)

    return reward_box


def make_island_box(island: str, rewards: [], grades: []):
    width, height = 1024 - icon_size[0] * 2 + margin * 2, icon_size[1] + margin * 2
    island_box = Image.new('RGBA', (width, height), background_color)

    # island
    island_image = get_image(island)
    island_image = island_image.resize(icon_size)

    island_box.paste(island_image, (margin, margin), island_image)

    # text
    drawable_image = ImageDraw.Draw(island_box)
    w, h = drawable_image.textsize(island, font=island_font)
    x, y = icon_size[0] + icon_gap * 4 + margin, (height - h) / 2
    drawable_image.text((x, y), island, fill=font_color, font=island_font)

    # reward
    rewards_box = make_rewards_box(rewards, grades)
    start_x, start_y = width - icon_size[0] * len(rewards) - icon_gap * (len(rewards) - 1) - margin, margin
    island_box.paste(rewards_box, (start_x, start_y), rewards_box)

    return island_box


def make_island_boxes(island_rewards_infoes: [[]]):
    width, height = 1024 - icon_size[0] * 2 + margin * 2, icon_size[1] * 3 + content_gap * 2 + margin * 6
    island_boxes = Image.new('RGBA', (width, height))

    for i in range(len(island_rewards_infoes)):
        item = island_rewards_infoes[i]

        island_box = make_island_box(item[0], [it[0] for it in item[1]], [it[-1] for it in item[1]])
        start_x, start_y = 0, (icon_size[1] + content_gap) * i
        island_boxes.paste(island_box, (start_x, start_y), island_box)

    return island_boxes


def make_island_content(island_rewards_infoes: [[]], time_text):
    width, height = 1024 - icon_size[0] * 2 + margin * 2, icon_size[1] * 3 + content_gap * 2 + icon_size[
        1] * 2 + margin * 6
    island_content = Image.new('RGBA', (width, height))

    # text
    drawable_image = ImageDraw.Draw(island_content)
    w, h = drawable_image.textsize(time_text, font=time_font)
    x, y = (width - w) / 2, h / 2
    drawable_image.text((x, y), time_text, fill=font_color, font=time_font)

    # image
    island_boxes = make_island_boxes(island_rewards_infoes)
    start_x, start_y = 0, icon_size[1] + content_gap
    island_content.paste(island_boxes, (start_x, start_y), island_boxes)

    return island_content


def make_daily_adventure_island(island_rewards_infoes: [[]], date_text):
    daily_adventure_island = None

    if len(island_rewards_infoes) == 6:
        daily_adventure_island_content = Image.new('RGBA', (window_size[0], window_size[1] * 2), title_back_color)

        # title
        drawable_image = ImageDraw.Draw(daily_adventure_island_content)
        w, h = drawable_image.textsize(date_text, font=title_font)
        x, y = (window_size[0] - w) / 2, h
        drawable_image.text((x, y), date_text, fill=title_color, font=title_font)

        island_content_1 = make_island_content(island_rewards_infoes[:3], "09:00/11:00/13:00")
        start_x, start_y = icon_size[0] - margin, icon_size[1] + content_gap
        daily_adventure_island_content.paste(island_content_1, (start_x, start_y), island_content_1)

        island_content_2 = make_island_content(island_rewards_infoes[3:], "19:00/21:00/23:00")
        start_x, start_y = icon_size[0] - margin, icon_size[1] * 7 + content_gap * 4
        daily_adventure_island_content.paste(island_content_2, (start_x, start_y), island_content_2)

    else:
        daily_adventure_island_content = Image.new('RGBA', window_size, title_back_color)

        # title
        drawable_image = ImageDraw.Draw(daily_adventure_island_content)
        w, h = drawable_image.textsize(date_text, font=title_font)
        x, y = (window_size[0] - w) / 2, h
        drawable_image.text((x, y), date_text, fill=title_color, font=title_font)

        island_content = make_island_content(island_rewards_infoes, "11:00/13:00/19:00/21:00/23:00")
        start_x, start_y = icon_size[0] - margin, icon_size[1] + content_gap
        daily_adventure_island_content.paste(island_content, (start_x, start_y), island_content)

    return daily_adventure_island_content


def get_adventure_island(date, is_weekend):
    reward_items = []

    if not is_weekend:
        reward_items = get_adventure_island_reward_info(date, 0)

    else:
        reward_items = get_adventure_island_reward_info(date, 0) + get_adventure_island_reward_info(date, 1)

    image = make_daily_adventure_island(reward_items, f"{date} 모험섬 일정")
    # link = f'./adventure_island/data/today/{date}.png'
    link = f'{path}/data/today/{date}.png'
    image.save(link)

    return link


if __name__ == "__main__":
    parse_adventure_island(authorization=f"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyIsImtpZCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyJ9.eyJpc3MiOiJodHRwczovL2x1ZHkuZ2FtZS5vbnN0b3ZlLmNvbSIsImF1ZCI6Imh0dHBzOi8vbHVkeS5nYW1lLm9uc3RvdmUuY29tL3Jlc291cmNlcyIsImNsaWVudF9pZCI6IjEwMDAwMDAwMDAwMDA1MTMifQ.KJSweBbQpwz7OcYwY_Fc9FJDmSBL_8y0KqNXKq3KMC6vIgy-Cmsfzi7klAyjIJLGRB2SeW9sq--QbafkIHBeWUVD7jROy8mhLvKlr8vLnGJ5IePGriBtC6IB-Ma6Wr1w4Upa0jwBDE7eRwk6FPX21wrXnalqk-MpYpTBmPp1MmcaNVCoxZliMRsNtfrFrQE0RnceerNsBAoj6blyIt7wH9IB5dHTzLYEDVXBA6rQeS8gBzYzcKC4yWDcHSas6es_JqCykp-w9HdaT20YXZW0te3knRl2VZ3oOsVmCmCoPk3cSHaqaleesmabKnuWPd7sT6FCvdKeuhfCNvMNAze9nA")
    link = get_adventure_island('2023-03-13', False)
    # path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    # api_key = read_json(path + "/data/key.json")["lostark"]["api_key"]
    # parse_adventure_island(authorization=f"Bearer {api_key}")

    # print(get_adventure_island('2023-03-11', False))
    # image = get_adventure_island(
    #     island=["하모니 섬", "죽음의 협곡", "고요한 안식의 섬", "하모니 섬", "죽음의 협곡", "고요한 안식의 섬"],
    #     reward=["카드", "실링", "골드", "카드", "실링", "골드"],
    #     double=False
    # )

    # image.show()
    # make_daily_adventure_island([
    #     ["스노우팡 아일랜드", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "실링"], ["전설", "고급", "희귀", "일반"]],
    #     ["기회의 섬", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "해적 주화", "실링"], ["전설", "고급", "희귀", "일반", "일반"]],
    #     ["스노우팡 아일랜드", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "해적 주화", "실링"], ["전설", "고급", "희귀", "일반", "일반"]]
    # ], "2023-03-11 모험섬 일정") \
    #     .save("D:/평일_테스트1.png")
    # .show()

    # make_daily_adventure_island([
    #     ["스노우팡 아일랜드", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "실링"], ["전설", "고급", "희귀", "일반"]],
    #     ["기회의 섬", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "해적 주화", "실링"], ["전설", "고급", "희귀", "일반", "일반"]],
    #     ["스노우팡 아일랜드", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "해적 주화", "실링"], ["전설", "고급", "희귀", "일반", "일반"]],
    #     ["스노우팡 아일랜드", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "실링"], ["전설", "고급", "희귀", "일반"]],
    #     ["기회의 섬", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "해적 주화", "실링"], ["전설", "고급", "희귀", "일반", "일반"]],
    #     ["스노우팡 아일랜드", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "해적 주화", "실링"], ["전설", "영웅", "희귀", "고급", "일반"]],
    # ], "2023-03-11 모험섬 일정") \
    #     .save("D:/주말_테스트1.png")
    # .show()
