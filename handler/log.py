from flask import Blueprint, render_template, session

bp = Blueprint('log', __name__)


@bp.route('/log')
def log():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    if session['status'] == '游客':
        return render_template('user/no.html', sname=session['user'])
    else:
        return render_template('log.html', sname=session['user'])
