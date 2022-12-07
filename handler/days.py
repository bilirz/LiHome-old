from flask import Blueprint, render_template, request, session
import time, pymongo
from bson.objectid import ObjectId

bp = Blueprint('days', __name__)
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
dbf = mongo['db_li']['days']


@bp.route('/days', methods=['GET', 'POST'])
def days():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if session['status'] == '游客':
        return render_template('user/no.html', sname=session['user'])
    else:
        if request.method == 'POST':
            document = {'name': session['user'],
                        'bname': request.values.get('bname'),
                        'why': request.values.get('why'),
                        'time': request.values.get('time'),
                        'wtime': time.strftime('%Y-%m-%d %H:%M:%S'),
                        }
            dbf.insert_one(document)
        return render_template('days/add.html', sname=session['user'], userinfos=mongo['db_li']['users'].find())


@bp.route('/days/text', methods=['GET', 'POST'])
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
        return render_template('days/text.html', sname=session['user'], doct=doct)
