from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.dbTil

# sched = BackgroundScheduler(daemon=True)
#
# sched.add_job(titleCrawling, 'cron', week='1-53', day_of_week='0-6', hour='21')
#
# sched.start()

@app.route('/')
def index():
    return render_template('index.html')

"""
페이지가 시작될 때 최근에 글이 추가된 목록을 뽑아와서 뿌려준다.
"""
@app.route('/sorted', methods=['GET'])
def sorting():
    news = list(db.recentTitle.find({}, {'_id':False}))
    return jsonify(news)


"""
영현님이 크롤링한 DB에서 주소들을 뽑아와서 현재 메인 페이지의 글 제목을 크롤링
텀을 두고 자동 실행 해야될 것 같다. delay가 없으면 크롤링을 제대로 처리 못한다.
"""
@app.route('/recentCrawling', methods=['GET'])
def titleCrawling():
    users = list(db.userInfo.find({}, {'_id': False}))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    for x in users:
        print(x)
        tempname = x['name']
        tempurl = x['url']

        if "velog" in tempurl:
            response = requests.get(tempurl)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.select_one('div.sc-emmjRN')
            if title is None:
                title = soup.select_one('div.sc-ktHwxA')
            if title is None:
                title = soup.select_one('div.sc-krDsej')
            if title is None:
                title = soup.select_one('div.sc-gHboQg')
        titles = title.select('a > h2')
        for title in titles:
            print(title.text)

        if "tistory" in tempurl:
            response = requests.get(tempurl)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            titles = soup.select('ul.list_horizontal > li')
            for title in titles:
                print(title.select_one('a.link_title').text)

        time.sleep(0.1)

    return jsonify(users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
