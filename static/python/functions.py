import datetime

from PIL import Image

from data.days import Day
from data.groups import Group
from data.users import User
from data.weeks import Week


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
        need_days = [days.index(1) + 1, days.index(1) + 1]
    else:
        need_days = []
        for i in range(6):
            if days[i]:
                need_days.append(i + 1)
    return need_days


def get_pars_list(db_sess, form: dict, need_days):
    audience_id = form['audience_id']
    st_date = form['st_date']
    en_date = form['en_date']
    weeks = db_sess.query(Week).filter(Week.audience_id == audience_id,
                                       st_date <= Week.week_end_date,
                                       Week.week_start_date <= en_date).all()
    days = [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]]
    for i in range(6):
        if i + 1 not in need_days:
            days[i] = []
    for week in weeks:
        for i in range(6):
            if not days[i]:
                continue
            day = week.days[i]
            if day.p1group:
                days[i][0] = None
            if day.p2group:
                days[i][1] = None
            if day.p3group:
                days[i][2] = None
            if day.p4group:
                days[i][3] = None
            if day.p5group:
                days[i][4] = None
            if day.p6group:
                days[i][5] = None
    return days


def create_week(db_sess, date: datetime.date, audience_id: int):
    needed_date = date - datetime.timedelta(days=date.weekday())
    if db_sess.query(Week).filter(Week.week_start_date == needed_date,
                                  Week.audience_id == audience_id).all():
        return
    week = Week(
        week_start_date=needed_date,
        week_end_date=needed_date + datetime.timedelta(days=6),
        audience_id=audience_id
    )
    for i in range(6):
        week.days.append(Day(date=needed_date + datetime.timedelta(days=i)))
    db_sess.add(week)
    db_sess.commit()


def load_week_by_group_form(db_sess, form: dict):
    print(form)
    days = sorted(form['days'])
    time = sorted([form['day0time'], form['day1time']])
    st_date = form['st_date']
    en_date = form['en_date']
    st_date: datetime.date
    en_date: datetime.date
    audience_id = form['audience_id']
    group = Group(
        subject=form['subject'],
        teacher_id=form['teacher_id'],
        audience_id=audience_id,
        course_start_date=st_date,
        course_end_date=en_date,
    )
    group.week_day0 = days[0]
    group.week_day1 = days[1]
    group.timeday0 = time[0] + 1
    group.timeday1 = time[1] + 1
    db_sess.add(group)
    db_sess.commit()
    while st_date <= en_date:
        week = db_sess.query(Week).filter(Week.week_start_date <= st_date,
                                          st_date <= Week.week_end_date,
                                          Week.audience_id == audience_id).first()
        if not week:
            create_week(db_sess, st_date, audience_id)
            week = db_sess.query(Week).filter(Week.week_start_date <= st_date,
                                              st_date <= Week.week_end_date,
                                              Week.audience_id == audience_id).first()
        if st_date.weekday() + 1 in days:
            day = week.days[st_date.weekday()]
            if len(set(days)) == 1:
                if 0 in time:
                    day.p1group = group.id
                if 1 in time:
                    day.p2group = group.id
                if 2 in time:
                    day.p3group = group.id
                if 3 in time:
                    day.p4group = group.id
                if 4 in time:
                    day.p5group = group.id
                if 5 in time:
                    day.p6group = group.id
            else:
                if st_date.weekday() + 1 == days[0]:
                    if time[0] == 0:
                        day.p1group = group.id
                    if time[0] == 1:
                        day.p1group = group.id
                    if time[0] == 2:
                        day.p1group = group.id
                    if time[0] == 3:
                        day.p1group = group.id
                    if time[0] == 4:
                        day.p1group = group.id
                    if time[0] == 5:
                        day.p1group = group.id
                else:
                    if time[1] == 0:
                        day.p1group = group.id
                    if time[1] == 1:
                        day.p1group = group.id
                    if time[1] == 2:
                        day.p1group = group.id
                    if time[1] == 3:
                        day.p1group = group.id
                    if time[1] == 4:
                        day.p1group = group.id
                    if time[1] == 5:
                        day.p1group = group.id

        st_date += datetime.timedelta(days=1)
    db_sess.commit()
    return True
