from flask import Blueprint, render_template, request, session
import time, pymongo

bp = Blueprint('energy', __name__)
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
dbf = mongo['db_li']['energy']


@bp.route('/energy/<name>', methods=['GET', 'POST'])
def name(name):
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if session['status'] == '游客':
        return render_template('user/no.html', sname=session['user'])
    else:
        data_list = []
        data_index_a = 0
        data_index_b = 0
        xAxis = []
        series = []
        if dbf.find_one({'name': session['user']}) is None:
            dbf.insert_one({
                'name': session['user'],
                'charts': []
            })
        if request.method == 'POST':
            new_value = {'$push':
                            {'charts': {'evalue': request.values.get('evalue'),
                                        'time': time.strftime('%Y-%m-%d %H:%M:%S')}}}
            dbf.update_one({'name': name}, new_value)
        for i in dbf.find({'name': name}):
            data_list = (i['charts'])

        for i in range(len(data_list)):
            xAxis.append(str(data_list[data_index_a]['time']))
            data_index_a += 1

        for i in range(len(data_list)):
            series.append(int(data_list[data_index_b]['evalue']))
            data_index_b += 1

        return render_template('energy/index.html', sname=session['user'], name=name, xAxis=xAxis, series=series)
