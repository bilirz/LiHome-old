from flask import Blueprint, render_template, request, session
import time, pymongo
from bson.objectid import ObjectId

bp = Blueprint('redblack', __name__)
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
dbf = mongo['db_li']['redblack']


@bp.route('/redblack', methods=['GET', 'POST'])
def redblack():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if session['status'] == '游客':
        return render_template('user/no.html', sname=session['user'])
    else:
        if request.method == 'POST':
            document = {'name': session['user'],
                        'bname': request.values.get('bname'),
                        'color': request.values.get('color'),
                        'text': request.values.get('text'),
                        'time': time.strftime('%Y-%m-%d %H:%M:%S'),
                        # 'comment':{'name':'null','text':'null'}
                        }
            dbf.insert_one(document)
        return render_template('redblack/add.html', sname=session['user'],
                               userinfos=mongo['db_li']['users'].find())


@bp.route('/redblack/text', methods=['GET', 'POST'])
def text():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if session['status'] == '游客':
        return render_template('user/no.html', sname=session['user'])
    else:
        doct = ''
        if request.method == 'GET':
            doct = dbf.find().sort('time', -1)
        elif request.method == 'POST':
            if request.values.get('type') == 'delete':
                dbf.delete_one({'_id': ObjectId(request.values.get('id'))})
            elif request.values.get('type') == 'comment':
                newvalue = {'$push':
                                {'comment': {'name': session['user'], 'text': request.values.get('text'),
                                             'time': time.strftime('%Y-%m-%d %H:%M:%S')}}}
                dbf.update_one({'_id': ObjectId(request.values.get('id'))}, newvalue)
        return render_template('redblack/text.html', sname=session['user'], doct=doct, state=0)


@bp.route('/redblack/text/red', methods=['GET', 'POST'])
def text_red():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if session['status'] == '游客':
        return render_template('user/no.html', sname=session['user'])
    else:
        doct = ''
        if request.method == 'GET':
            doct = dbf.find({'color': '红'}).sort('time', -1)
        elif request.method == 'POST':
            if request.values.get('type') == 'delete':
                dbf.delete_one({'_id': ObjectId(request.values.get('id'))})
            elif request.values.get('type') == 'comment':
                newvalue = {'$push':
                                {'comment': {'name': session['user'], 'text': request.values.get('text'),
                                             'time': time.strftime('%Y-%m-%d %H:%M:%S')}}}
                dbf.update_one({'_id': ObjectId(request.values.get('id'))}, newvalue)
        return render_template('redblack/text.html', sname=session['user'], doct=doct, state=1)

@bp.route('/redblack/text/black', methods=['GET', 'POST'])
def text_black():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if session['status'] == '游客':
        return render_template('user/no.html', sname=session['user'])
    else:
        doct = ''
        if request.method == 'GET':
            doct = dbf.find({'color': '黑'}).sort('time', -1)
        elif request.method == 'POST':
            if request.values.get('type') == 'delete':
                dbf.delete_one({'_id': ObjectId(request.values.get('id'))})
            elif request.values.get('type') == 'comment':
                newvalue = {'$push':
                                {'comment': {'name': session['user'], 'text': request.values.get('text'),
                                             'time': time.strftime('%Y-%m-%d %H:%M:%S')}}}
                dbf.update_one({'_id': ObjectId(request.values.get('id'))}, newvalue)
        return render_template('redblack/text.html', sname=session['user'], doct=doct, state=2)
