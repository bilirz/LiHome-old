from flask import Blueprint, render_template, session

import pymongo

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    if session.get('user') is None:
        session['user'] = {
            'id': -1,
            'name': 0,
            'status': 0
        }
    if session['user']['status'] == 0:
        return render_template('user/status_error.html', session=session['user'])
    else:
        return render_template('index.html', session=session['user'])
