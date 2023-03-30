import flask
from flask import request, jsonify

from static.python.functions import DecodeDate, get_week_audience, DateEncoder, get_week_teacher, get_week_group
from . import db_session
#from . import News
from .audiences import Audience

blueprint = flask.Blueprint(
    'week_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/audiences_week/<int:audience_id>')
def get_week(audience_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if not all(key in request.json for key in ['date']):
        return jsonify({'error': 'Bad request'})
    try:
        date = DecodeDate(request.json['date'])
    except Exception:
        return jsonify({'error': 'Data must be in "%Y-%m-%d" format'})
    week = get_week_audience(db_session.create_session(), audience_id, date)
    return jsonify({'audiences': [{"id": week.audience.id, "name": week.audience.name, "week": {
        'id': week.id, 'start_date': week.week_start_date, 'end_date': week.week_end_date,
        'days': [{DateEncoder(day.date): {"pars": [{"subject": par.subject,
                                                    "teacher": {"name": par.teacher.name,
                                                                "surname": par.teacher.surname,
                                                                "fathername": par.teacher.otchestvo,
                                                                "email": par.teacher.email
                                                                }} if par else
                                                   {'subject': None, "teacher": None}
                                                   for par in day.pars]}} for day in week.days]
    }}]})


@blueprint.route('/api/audiences_week')
def get_all():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if not all(key in request.json for key in ['date']):
        return jsonify({'error': 'Bad request'})
    try:
        date = DecodeDate(request.json['date'])
    except Exception:
        return jsonify({'error': 'Data must be in "%Y-%m-%d" format'})
    db_sess = db_session.create_session()
    weeks = []
    arr = []
    for audience in db_sess.query(Audience).filter(Audience.is_eventable == False).all():
        week = get_week_audience(db_sess, audience.id, date)
        arr.append({"id": week.audience.id, "name": week.audience.name, "week": {
        'id': week.id, 'start_date': week.week_start_date, 'end_date': week.week_end_date,
        'days': [{DateEncoder(day.date): {"pars": [{"subject": par.subject,
                                                    "teacher": {"name": par.teacher.name,
                                                                "surname": par.teacher.surname,
                                                                "fathername": par.teacher.otchestvo,
                                                                "email": par.teacher.email
                                                                }} if par else
                                                   {'subject': None, "teacher": None}
                                                   for par in day.pars]}} for day in week.days]
    }})
    return jsonify({'audiences': arr})
