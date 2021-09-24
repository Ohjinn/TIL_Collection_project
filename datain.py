from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client.dbTil

recentTitle = [
    {"name": "서지희", "title": "9월 13일"},
    {"name": "서지희", "title": "9월 14일"},
    {"name": "서지희", "title": "9월 15일"},
    {"name": "서지희", "title": "9월 16일"},
    {"name": "서지희", "title": "9월 17일"},
    {"name": "서지희", "title": "9월 23일"},
    {"name": "서지희", "title": "9월 23일"},
    {"name": "서지희", "title": "1 주차 회고록"},
    {"name": "서지희", "title": "프로젝트 1"},

    {"name": "권나연", "title": "[내일배움캠프] 1일차 TIL"},
    {"name": "권나연", "title": "[내일배움캠프] 2일차 TIL"},
    {"name": "권나연", "title": "[내일배움캠프] 3일차 TIL"},
    {"name": "권나연", "title": "[내일배움캠프] 4일차 TIL"},
    {"name": "권나연", "title": "[내일배움캠프] 5일차 TIL"},
    {"name": "권나연", "title": "[내일배움캠프] 6일차 TIL"},
    {"name": "권나연", "title": "[내일배움캠프] 7일차 TIL"},
    {"name": "권나연", "title": "[내일배움캠프] 8일차 TIL"},
    {"name": "권나연", "title": "[내일배움캠프] 9일차 TIL"},
    {"name": "권나연", "title": "[내일배움캠프] 10일차 TIL"},
    {"name": "권나연", "title": "[내일배움캠프] 11일차 TIL"},
    {"name": "권나연", "title": "[내일배움캠프] 프로젝트 SA"},
    {"name": "권나연", "title": "[내일배움캠프] 1주차 WIL"},

    {"name": "윤영현", "title": "내일배움캠프 1일차 개발일지"},
    {"name": "윤영현", "title": "내일배움캠프 2일차 개발일지"},
    {"name": "윤영현", "title": "내일배움캠프 격변의 3일차!"},
    {"name": "윤영현", "title": "내일배움캠프 4일차 개발일지"},
    {"name": "윤영현", "title": "1주차 WIL"},
    {"name": "윤영현", "title": "내일배움캠프 6일차 개발일지"},
    {"name": "윤영현", "title": "내일배움캠프 7일차 개발일지"},
    {"name": "윤영현", "title": "내일배움캠프 8일차 개발일지"},

    {"name": "장호진", "title": "TIL - 1"},
    {"name": "장호진", "title": "TIL - 6"},
    {"name": "장호진", "title": "TIL-2"},
    {"name": "장호진", "title": "TIL-3"},
    {"name": "장호진", "title": "TIL-4"},
    {"name": "장호진", "title": "TIL-5"},
    {"name": "장호진", "title": "TIL-7"},
    {"name": "장호진", "title": "TIL-8"},

]
db.recentTitle.insert_many(recentTitle)


userInfo = [
        {"name": "서지희", "url": "https://velog.io/@diheet", "pic":""},
        {"name": "권나연", "url": "https://velog.io/@hellonayeon", "pic":""},
        {"name": "윤영현", "url": "https://goodtoseeyou.tistory.com", "pic":""},
        {"name": "장호진", "url": "https://ohjinn.tistory.com", "pic":""},
 ]
db.userInfo.insert_many(userInfo)