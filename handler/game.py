from flask import Blueprint, render_template, request, session
import time, pymongo, random

bp = Blueprint('game', __name__)
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
dbf = mongo['db_li']['game']


def create():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if session['status'] == '游客':
        return render_template('user/no.html', sname=session['user'])
    else:
        if dbf.find_one({'name': session['user']}) is None:
            dbf.insert_one({'name': session['user'], 'coin': 0})


@bp.route('/game', methods=['GET', 'POST'])
def game():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if session['status'] == '游客':
        return render_template('user/no.html', sname=session['user'])
    else:
        create()
        if request.method == 'POST':
            bcoin = random.randint(1, 2)
            dbf.update_one({'name': session['user'], },
                           {'$set': {'coin': dbf.find_one(
                               {'name': session['user']})['coin']
                                             + dbf.find_one({'name': request.values.get('bname')})['coin'] / bcoin}})
            dbf.update_one({'name': request.values.get('bname'), },
                           {'$set': {'coin': dbf.find_one(
                               {'name': request.values.get('bname')})['coin']
                                             - dbf.find_one({'name': request.values.get('bname')})['coin'] / bcoin}})
            time.sleep(10)
            # print(dbf.find_one({'name':request.values.get('bname')}))
        return render_template('game/index.html', sname=session['user'], userinfos=mongo['db_li']['users'].find())


@bp.route('/game/coin', methods=['GET', 'POST'])
def coin():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if session['status'] == '游客':
        return render_template('user/no.html', sname=session['user'])
    else:
        create()
        if request.method == 'POST':
            dbf.update_one({'name': session['user'], }, {
                '$set': {'coin': dbf.find_one({'name': session['user']})['coin'] + random.randint(100, 1000)}})
            time.sleep(10)
        return render_template('game/coin.html', sname=session['user'])


@bp.route('/game/rank', methods=['GET'])
def rank():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if session['status'] == '游客':
        return render_template('user/no.html', sname=session['user'])
    else:
        l = []
        m = []
        for i in dbf.find().sort('coin', 1):
            l.append(i['name'])
        for i in dbf.find().sort('coin', 1):
            m.append(i['coin'])
        return render_template('game/rank.html', sname=session['user'], all=dbf.find().sort('coin', -1), l=l, m=m)
