from flask import Blueprint, render_template, session, redirect
import pymongo

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
        redblack = mongo['db_li']['redblack'].find().sort('time', -1).limit(3)
        days = mongo['db_li']['days'].find().sort('time', -1).limit(3)
        pk = mongo['db_li']['pk'].find().sort('coin', -1).limit(3)
        return render_template('index.html', sname=session['user'], users=users, redblack=redblack, days=days, pk=pk)
