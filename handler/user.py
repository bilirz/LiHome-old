import hashlib
import pymongo
import time
import urllib

from flask import Blueprint, render_template, request, session, redirect, jsonify

bp = Blueprint('user', __name__)
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
dbf = mongo['db_li']['users']


def md5(a, b):
    md = hashlib.md5()
    md.update(str(a).encode('utf-8'))
    md.update(str(b).encode('utf-8'))
    return md.hexdigest()


@bp.route('/user/login', methods=['GET', 'POST'])
def login():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    dbf.delete_one({'name': None})
    if request.method == 'POST':
        if dbf.find_one({'name': request.values.get('name')}) is not None:
            if dbf.find_one({'name': request.values.get('name')})['password'] == md5(request.values.get('password'),
                                                                                     dbf.find_one({
                                                                                                      'name': request.values.get(
                                                                                                              'name')})[
                                                                                         'time']):
                session['user'] = request.values.get('name')
                session['status'] = dbf.find_one({"name": request.values.get('name')})['status']
        elif dbf.find_one({'name': request.values.get('name')}) is None:
            print(request.values.get('password'))
    return render_template('user/login.html', sname=session['user'])


@bp.route('/user/register', methods=['GET', 'POST'])
def register():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if request.method == 'POST':
        session['user'] = '游客'
        dbf.delete_one({'name': None})
        if request.values.get('password') == request.values.get('again'):
            if dbf.find_one({'name': request.values.get('name')}) is not None:
                return jsonify({'errmsg': '账号名已被注册'})
            elif dbf.find_one({'name': request.values.get('name')}) is None:
                time_ = time.strftime('%Y-%m-%d %H:%M:%S')
                document = {'name': request.values.get('name'),
                            'password': md5(request.values.get('password'), time_),
                            'status': "游客",
                            'time': time_,
                            }
                dbf.insert_one(document)
            return jsonify({'errmsg': '注册成功！请重新登录~'})
        else:
            return jsonify({'errmsg': '两次输入密码不一致'})
    return render_template('user/register.html', sname=session['user'])


@bp.route('/user/out', methods=['GET', 'POST'])
def out():
    session['user'] = '游客'
    session['status'] = '游客'
    return redirect('/user/login')


@bp.route('/user/<name>', methods=['GET', 'POST'])
def index(name):
    return render_template('user/index.html',
                           sname=session['user'],
                           infos=dbf.find_one({'name': urllib.parse.unquote(name)}),
                           redinfos=mongo['db_li']['redblack'].find(
                               {'$and': [{'bname': urllib.parse.unquote(name)}, {'color': '红'}]}).sort('time', -1),
                           redinfos_count=mongo['db_li']['redblack'].count_documents(
                               {'$and': [{'bname': urllib.parse.unquote(name)}, {'color': '红'}]}),
                           blackinfos=mongo['db_li']['redblack'].find(
                               {'$and': [{'bname': urllib.parse.unquote(name)}, {'color': '黑'}]}).sort('time', -1),
                           blackinfos_count=mongo['db_li']['redblack'].count_documents(
                               {'$and': [{'bname': urllib.parse.unquote(name)}, {'color': '黑'}]}),
                           wredinfos=mongo['db_li']['redblack'].find(
                               {'$and': [{'name': urllib.parse.unquote(name)}, {'color': '红'}]}).sort('time', -1),
                           wredinfos_count=mongo['db_li']['redblack'].count_documents(
                               {'$and': [{'name': urllib.parse.unquote(name)}, {'color': '红'}]}),
                           wblackinfos=mongo['db_li']['redblack'].find(
                               {'$and': [{'name': urllib.parse.unquote(name)}, {'color': '黑'}]}).sort('time', -1),
                           wblackinfos_count=mongo['db_li']['redblack'].count_documents(
                               {'$and': [{'name': urllib.parse.unquote(name)}, {'color': '黑'}]})
                           )
