import datetime

from PIL import Image

from data.users import User
from data.weeks import Week

ST_message = {'status': 404, 'text': ''}
DAYS = {0: 'Пн', 1: "Вт", 2: "Ср", 3: "Чт", 4: "Пт", 5: "Сб"}
PARS_TIMES = {0: '8:30-10:00', 1: '11:40-13:10', 2: '13:20-14:50', 3: '15:00-16:30', 4: '16:40-18:10', 5: '18:15-19:45'}


def DateEncoder(date: datetime.date):
    return date.strftime("%Y-%m-%d")


def DecodeDate(string: str):
    return datetime.datetime.strptime(string, "%Y-%m-%d").date()


def create_main_admin(db_sess):
    res = db_sess.query(User).all()
    if res:
        return
    user = User(
        id=1,
        email='main_admin@mail.ru',
        role=4,
        img='img/users/1.jpg'
    )
    Image.open('static/img/admin.jpg').save('static/img/users/1.jpg')
    user.set_password('111')
    db_sess.add(user)
    db_sess.commit()


def get_need_days(form: dict) -> list:
    days = [form['day0'], form['day1'], form['day2'], form['day3'], form['day4'], form['day5']]
    le = len(list(filter(lambda x: x, days)))
    if le == 1:
        need_days = [days.index(1), days.index(1)]
    else:
        need_days = []
        for i in range(6):
            if days[i]:
                need_days.append(i)
    return need_days


def get_pars_list(db_sess, form: dict, need_days):
    audience_id = form['audience_id']
    st_date = form['st_date']
    en_date = form['en_date']
    weeks = db_sess.query(Week).filter(Week.audience_id == audience_id,
                                       st_date <= Week.week_end_date, Week.week_start_date <= en_date).all()
    days = [[True, True, True, True, True, True], [True, True, True, True, True, True]]
    if not weeks:
        return days
    for week in weeks:
        for i in range(6):
            if i not in need_days:
                continue
            day = week.days[i]
            days[i][0] *= (not day.p1group)
            days[i][1] *= (not day.p2group)
            days[i][2] *= (not day.p3group)
            days[i][3] *= (not day.p4group)
            days[i][4] *= (not day.p5group)
            days[i][5] *= (not day.p6group)
    return days
