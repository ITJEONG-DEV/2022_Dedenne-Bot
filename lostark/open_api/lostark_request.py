import urllib.parse

from util import *
import requests

main_url = "https://developer-lostark.game.onstove.com"


# Get info
def get_GET_headers(json_link="D:/2022_Dedenne-Bot/json/info.json"):
    authorization = parse_json(json_link)["lostark"]["apikeyauth"]
    return {'accept': 'application/json', 'authorization': authorization}

def get_POST_headers(json_link="D:/2022_Dedenne-Bot/json/info.json"):
    authorization = parse_json(json_link)["lostark"]["apikeyauth"]
    return {'accept': 'application/json', 'authorization': authorization, 'Content-Type': 'application/json'}

def get_engraving_info(json_link="D:/2022_Dedenne-Bot/json/engraves.json"):
    return parse_json(json_link)


# GET apis
def get_characters(character_name):
    request_url = main_url + "/characters/" + character_name + "/siblings"
    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_profiles(character_name):
    request_url = main_url + "/armories/characters/" + character_name + "/profiles"
    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_equipment(character_name):
    request_url = main_url + "/armories/characters/" + character_name + "/equipment"
    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_avatars(character_name):
    request_url = main_url + "/armories/characters/" + character_name + "/avatars"
    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_combat_skiils(character_name):
    request_url = main_url + "/armories/characters/" + character_name + "/combat-skills"
    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_engravings(character_name):
    request_url = main_url + "/armories/characters/" + character_name + "/engravings"
    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_cards(character_name):
    request_url = main_url + "/armories/characters/" + character_name + "/cards"
    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_gems(character_name):
    request_url = main_url + "/armories/characters/" + character_name + "/gems"
    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_colosseums(character_name):
    request_url = main_url + "/armories/characters/" + character_name + "/colosseums"
    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_collectibles(character_name):
    request_url = main_url + "/armories/characters/" + character_name + "/collectibles"
    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_armories(character_name):
    contents = {
        "profiles": get_profiles(character_name),
        "equipment": get_equipment(character_name),
        "avatars": get_avatars(character_name),
        "combat-skills": get_combat_skiils(character_name),
        "engravings": get_engravings(character_name),
        "cards": get_cards(character_name),
        "gems": get_gems(character_name),
        "colosseums": get_collectibles(character_name),
        "collectibles": get_collectibles(character_name)
    }
    return contents


def get_item_id(keyword):
    engraving_items = get_engraving_info()

    keyword_dict = {
        "스커": "스트라이커",
        "디트": "디스트로이어",
        "배마": "배틀마스터",
        "알카": "아르카나",
        "데헌": "데빌헌터",
        "가짜건슬": "데빌헌터",
        "홀나": "홀리나이트",

        "구동": "구슬동자",
        "강무": "강화 무기",
        "결대": "결투의 대가",
        "극의체술": "극의:",
        "급타": "급소타격",
        "고기": "고독한 기사",
        "기대": "기습의 대가",
        "달소": "달의 소리",
        "달저": "달인의 저력",
        "돌대": "돌격대장",
        "마효증": "마나 효율 증가",
        "마흐": "마나의 흐름",
        "부뼈": "부러진 뼈",
        "분망": "분노의 망치",
        "번분": "번개의 분노",
        "사시": "사냥의 시간",
        "선필": "선수필승",
        "시집": "시선 집중",
        "아기": "아르데타인의 기술",
        "안상": "안정된 상태",
        "약무": "약자 무시",
        "예둔": "예리한 둔기",
        "저받": "저주받은",
        "전태": "전투 태세",
        "절구": "절실한 구원",
        "정단": "정밀 단도",
        "정흡": "정기 흡수",
        "중수": "중력 수련",
        "중착": "중갑 착용",
        "진용": "진실된 용맹",
        "질증": "질량 증가",
        "최마증": "최대 마나 증가",
        "충단": "충격 단련",
        "타대": "타격의 대가",
        "폭전": "폭발물 전문가",
        "피메": "피스메이커"
    }

    if keyword in keyword_dict.keys():
        keyword = keyword_dict[keyword]

    target = []
    for engraved in engraving_items:
        if keyword in engraved["name"]:
            target.append(engraved["itemId"])

    return target


def get_engraving_item(item_name):
    item_ids = get_item_id(item_name)

    request_url = main_url + "/markets/items/"

    contents = []
    for item_id in item_ids:
        response = requests.get(request_url + str(item_id), headers=get_GET_headers())

        contents.append(response.json())

    return contents


def get_news():
    request_url = main_url + "/news/events"

    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_markets(itemId):
    request_url = main_url + "/markets/items/" + str(itemId)

    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_challenge_abyss_dungeons():
    request_url = main_url + "/gamecontents/challenge-abyss-dungeons"

    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_challenge_guardian_raids():
    request_url = main_url + "/gamecontents/challenge-guardian-raids"

    response = requests.get(request_url, headers=get_GET_headers())

    return response.json()


def get_callendar():
    request_url = main_url + "/gamecontents/calendar"

    response = requests.get(request_url, headers=get_GET_headers())

    dict = {}

    for item in response.json():
        key = item["CategoryName"]

        if key not in dict.keys():
            dict[key] = []

        dict[key].append(item)

    return dict


def get_gems(name="7레벨 홍염의 보석", character_class=""):
    data_dict = {}

    data_dict["ItemLevelMin"] = 0
    data_dict["ItemLevelMax"] = 0
    data_dict["ItemGradeQuality"] = 0

    data_dict["SkillOptions"] = [{}]
    data_dict["SkillOptions"][0]["FirstOption"] = None
    data_dict["SkillOptions"][0]["SecondOption"] = None
    data_dict["SkillOptions"][0]["MinValue"] = None
    data_dict["SkillOptions"][0]["MaxValue"] = None

    data_dict["EtcOptions"] = [{}]
    data_dict["EtcOptions"][0]["FirstOption"] = None
    data_dict["EtcOptions"][0]["SecondOption"] = None
    data_dict["EtcOptions"][0]["MinValue"] = None
    data_dict["EtcOptions"][0]["MaxValue"] = None

    data_dict["Sort"] = "BUY_PRICE"
    data_dict["CategoryCode"] = 210000
    data_dict["CharacterClass"] = character_class
    data_dict["ItemTier"] = 3
    data_dict["ItemGrade"] = ""
    data_dict["ItemName"] = name
    data_dict["PageNo"] = 0
    data_dict["SortCondition"] = "ASC"

    data = json.dumps(data_dict)

    request_url = main_url + "/auctions/items"

    response = requests.post(request_url, headers=get_POST_headers(), data=data)

    return response.json()


if __name__ == "__main__":
    # print(get_headers("D:/2022_Dedenne-Bot/json/info.json"))

    # print(get_characters("데덴네귀여워"))
    # print(get_armories("데덴네귀여워"))
    # print(get_engraving_item("소서리스"))

    # data = get_markets(355530118)

    # print(data[0]['ToolTip'].replace("\r",""))

    # data = get_callendar()

    # print(get_callendar().keys())
    # print(len(data["모험 섬"]))

    # import datetime
    # print(datetime.datetime.strptime("2023-03-11", "%Y-%m-%d"))

    print(get_gems())

    # print(get_profiles("데덴네귀여워"))
