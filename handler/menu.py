from flask import Blueprint, render_template, session, request
import time, pymongo
from bson.objectid import ObjectId

bp = Blueprint('menu', __name__)
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
dbf = mongo['db_li']['menu']

@bp.route('/menu', methods=['GET', 'POST'])
def menu():
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
            if request.values.get('type') == 'write':
                document = {'name': session['user'],
                        'text': request.values.get('text'),
                        "date": request.values.get('date'),
                        'time': time.strftime('%Y-%m-%d %H:%M:%S'),
                        }
                dbf.insert_one(document)
            elif request.values.get('type') == 'delete':
                dbf.delete_one({'_id': ObjectId(request.values.get('id'))})
            elif request.values.get('type') == 'comment':
                newvalue = {'$push':
                                {'comment': {'name': session['user'], 'text': request.values.get('text'),
                                             'time': time.strftime('%Y-%m-%d %H:%M:%S')}}}
                dbf.update_one({'_id': ObjectId(request.values.get('id'))}, newvalue)
        return render_template('menu.html', sname=session['user'], doct=doct)

