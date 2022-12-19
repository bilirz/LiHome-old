import pymongo
from flask import Blueprint, render_template, session

bp = Blueprint('index', __name__)
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017/')


@bp.route('/')
def index():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if session['status'] == '游客':
        return render_template('user/no.html', sname=session['user'])
    else:
        mongo['db_li']['users'].delete_one({'name': None})
        users = mongo['db_li']['users'].find()
        users_awards_all = mongo['db_li']['users'].find()
        users_awards_wred = mongo['db_li']['users'].find()
        users_awards_wblack = mongo['db_li']['users'].find()
        user_all = {'0': 0}
        user_wred = {'0': 0}
        user_wblack = {'0': 0}
        for user in users_awards_all:
            award_all = mongo['db_li']['redblack'].count_documents({'name': user['name']})
            user_all[user['name']] = award_all

        for user in users_awards_wred:
            award_wred = mongo['db_li']['redblack'].count_documents(
                {'$and': [{'bname': user['name']}, {'color': '红'}]})
            user_wred[user['name']] = award_wred

        for user in users_awards_wblack:
            award_wblack = mongo['db_li']['redblack'].count_documents(
                {'$and': [{'bname': user['name']}, {'color': '黑'}]})
            user_wblack[user['name']] = award_wblack

        redblack = mongo['db_li']['redblack'].find().sort('time', -1).limit(3)
        days = mongo['db_li']['days'].find().sort('time', -1).limit(4)
        pk = mongo['db_li']['pk'].find().sort('coin', -1).limit(3)
        return render_template('index.html', sname=session['user'], users=users, redblack=redblack, days=days, pk=pk,
                               award_all=max(user_all, key=lambda x: user_all[x]),
                               award_wred=max(user_wred, key=lambda x: user_wred[x]),
                               award_wblack=max(user_wblack, key=lambda x: user_wblack[x]),
                               mottos = mongo['db_li']['motto'].find().sort('time', -1).limit(3),
                               mottos_first = mongo['db_li']['motto'].find().sort('time', -1).limit(1))
