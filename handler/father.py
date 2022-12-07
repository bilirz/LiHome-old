from flask import Blueprint, render_template, session

bp = Blueprint('father', __name__)


@bp.route('/father')
def father():
    if session.get('user') is None:
        session['user'] = '游客'
        session['status'] = '游客'
    return render_template('father.html', sname=session['user'])
