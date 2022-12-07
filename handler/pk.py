from flask import Blueprint, render_template, session, request
import pymongo, time
from bson.objectid import ObjectId

bp = Blueprint('pk', __name__)
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
dbf = mongo['db_li']['pk']


@bp.route('/pk', methods=['GET', 'POST'])
def pk():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if session['status'] == '游客':
        return render_template('user/no.html', sname=session['user'])
    else:
        if request.method == 'POST':
            document = {'name': session['user'],
                        'bname': request.values.get('bname'),
                        'promise': request.values.get('promise'),
                        'dl': request.values.get('dl'),
                        'award': request.values.get('award'),
                        'punish': request.values.get('punish'),
                        'notary': request.values.get('notary'),
                        'state': 0,
                        'time': time.strftime('%Y-%m-%d %H:%M:%S'),
                        }
            dbf.insert_one(document)
        return render_template('pk/add.html', sname=session['user'], bnames=mongo['db_li']['users'].find(),
                               notarys=mongo['db_li']['users'].find())


@bp.route('/pk/text', methods=['GET', 'POST'])
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
            elif request.values.get('type') == 'pk':
                if dbf.find_one({'_id': ObjectId(request.values.get('id'))})['bname'] == session['user']:
                    dbf.update_one({'_id': ObjectId(request.values.get('id'))}, {'$set': {'state': 1}})
                else:
                    return "无权限"
        return render_template('pk/text.html', sname=session['user'], doct=doct)


@bp.route('/pk/pact/<id>', methods=['GET', 'POST'])
def pact(id):
    return render_template('pk/pact.html', sname=session['user'], doct=dbf.find_one({'_id': ObjectId(id)}))
