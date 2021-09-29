from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import requests
import time
from bs4 import BeautifulSoup
from flask_apscheduler import APScheduler
import urllib

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())

client = MongoClient("mongodb://localhost:27017/")
db = client.dbTil

"""
주기적 실행을 위한 flask-apscheduler 라이브러리 (https://viniciuschiele.github.io/flask-apscheduler/rst/usage.html)
"""
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('interval', id='autocraw', seconds=900, misfire_grace_time=900)
def autocraw():
    titleCrawling()

@scheduler.task('interval', id='autoPiccraw', seconds=3600, misfire_grace_time=900)
def autoPiccraw():
    getPic()


@app.route('/')
def index():
    return render_template('index.html')

def getPic():
    users = list(db.userInfo.find({}, {'_id': False}))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    for one in users:
        name = one['name']
        url = one['url']
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        image = soup.select_one('meta[property="og:image"]')['content']

        imgUrl = image

        # urlretrieve는 다운로드 함수
        urllib.request.urlretrieve(imgUrl, "static/images/" + name + '.jpg')

        db.userInfo.update_one({'name': name}, {'$set': {'pic': '../static/images/' + name + '.jpg'}})


"""
첫 로딩시 velog 정보와 tistory 정보를 나눠서 view로 쏴주는 컨트롤러
"""
@app.route('/sorted', methods=['GET'])
def sorting():
    news = list(db.userStack.find({}, {'_id':False}))
    news.reverse()
    velogcards = []
    tistorycards = []
    for x in news:
        tempname = x['name']
        tempurl = db.userInfo.find_one({'name' : tempname}, {'_id':False})['url']
        if 'velog' in tempurl:
            velogcards.append(db.userInfo.find_one({'name':tempname}, {'_id':False}))
        elif 'tistory' in tempurl:
            tistorycards.append(db.userInfo.find_one({'name':tempname}, {'_id':False}))

    return jsonify({'velogcards' :velogcards, 'tistorycards' : tistorycards})

"""
웹 크롤링을 위한 컨트롤러. 일정시간마다 실행되게 하는 구현 필
"""
def titleCrawling():
    print('autoCrawling')
    users = list(db.userInfo.find({}, {'_id': False}))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    newlist = []
    for x in users:
        tempname = x['name']
        tempurl = x['url']

        #벨로그 크롤링
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
            if title is None:
                title = soup.select_one('div.sc-eilVRo')
            if title is None:
                title = soup.select_one('div.sc-jbKcbu')

            titles = title.select('a > h2')
            for title in titles:
                newlist.append({'name': tempname, 'title': title.text})

        #티스토리 크롤링
        if "tistory" in tempurl:
            response = requests.get(tempurl)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.select_one('ul.list_horizontal')
            if title is None:
                title = soup.select('ul.list_category > li')
                for titles in title:
                    detail_title = titles.select_one('div.info > strong.name')
                    newlist.append({'name': tempname, 'title': detail_title.text})

            else:
                title = title.select('li')
                for titles in title:
                    detail_title = titles.select_one('div.box_contents > a')
                    newlist.append({'name': tempname, 'title': detail_title.text})

        #크롤링 페이지를 켜기 위한 딜레이
        time.sleep(0.5)

    #최근에 저장한 타이틀 목록을 불러오고 또 최근에 글을 쓴 사람이 뒤쪽 순번에 들어가있는 db를 불러온다.
    dbtitlelist = list(db.recentTitle.find({}, {'_id': False}))
    # dbuserstack = list(db.userStack.find({}, {'_id':False}))

    #만약 DB에 없는 제목 생긴 사람이 있으면 이름을 newstack에 저장
    newstack = []
    for x in newlist:
        tempname = x['name']
        temptitle = x['title']
        if x not in dbtitlelist:
            #임의의 제목 리스트가 DB리스트에 없으면 db리스트에 넣어주면서 최근에 변경이 감지된 사람을 스택에 저장한다.
            db.recentTitle.insert_one(x)
            if tempname not in newstack:
                print('now inserting name into stack')
                newstack.append(tempname)

    #userStack에서 최근 글이 쓰여진 사람을 목록에서 없애고 뒤에 붙임.
    for x in newstack:
        tempname = x
        db.userStack.delete_one({'name' : tempname})
        db.userStack.insert_one({'name' : tempname})




#검색
@app.route('/search', methods=['GET'])
def search():
    txt = request.args.get("txt")
    userdb = db.userInfo.find_one({'name':txt},{'_id':False})
    return jsonify(userdb)

#리뷰
@app.route('/review', methods=['POST'])
def modalReview():

    user_receive = request.form['user_give']
    review_receive = request.form['review_give']

    doc = {

        'user':user_receive,
        'review':review_receive

    }
    db.tilreview.insert_one(doc)

    return jsonify({'msg':'저장되었습니다!'})

@app.route('/reviewTarget', methods=['POST'])
def modalTarget():
    target_receive = request.form['target_give']

    doc = {

        'target': target_receive

    }
    db.tilreview.insert_one(doc)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

