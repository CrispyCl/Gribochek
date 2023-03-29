import datetime
from copy import deepcopy

from PIL import Image

from data import db_session
from data.audiences import Audience
from data.days import Day
from data.groups import Group
from data.users import User
from data.weeks import Week
from static.python.vClassFunctions import get_day, get_audience
from static.python.variables import vWeek, vDay


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


def get_teacher_par_list(db_sess, form: dict):
    def add_timetables(w1, w2):
        week1 = deepcopy(w1)
        for day1, day2 in zip(week1.days, w2.days):
            for i, p2 in enumerate(day2.pars):
                if p2:
                    day1.pars[i] = p2
        # for day, d2 in zip(week1.days, w2.days):
        #     print(day.id, d2.id)
        #     print(day.pars, d2.pars)
        # print()
        return week1
    teacher_id = form['teacher_id']
    st_date = DecodeDate(form['st_date'])
    en_date = DecodeDate(form['en_date'])
    need = get_need_days(form)
    day0 = [1, 2, 3, 4, 5, 6]
    day1 = [1, 2, 3, 4, 5, 6]
    groups = db_sess.query(Group).filter(Group.teacher_id == teacher_id,
                                         Group.is_mer == False).all()

    if not groups:
        return [day0, day1]
    if len(groups) == 1:
        week = get_week_group(db_sess, groups[0].id, date=st_date)
    else:
        g1 = get_week_group(db_sess, groups[0].id, date=st_date)
        g2 = get_week_group(db_sess, groups[1].id, date=st_date)
        week = add_timetables(g1, g2)
    for gr in groups[2:]:
        week = add_timetables(week, get_week_group(db_sess, gr.id, date=st_date))
    while st_date <= en_date:
        if st_date.weekday() == 0:
            if len(groups) == 1:
                week = get_week_group(db_sess, groups[0].id, date=st_date)
            else:
                g1 = get_week_group(db_sess, groups[0].id, date=st_date)
                g2 = get_week_group(db_sess, groups[1].id, date=st_date)
                week = add_timetables(g1, g2)
            for gr in groups[2:]:
                week = add_timetables(week, get_week_group(db_sess, gr.id, date=st_date))
        if st_date.weekday() + 1 not in need:
            st_date += datetime.timedelta(days=1)
            continue
        day = week.days[st_date.weekday()].pars
        if need[0] == need[1]:
            for i, par in enumerate(day):
                if par:
                    day0[i] = None
                    day1[i] = None
        else:
            for i, par in enumerate(day):
                if par:
                    if st_date.weekday() + 1 == need[0]:
                        day0[i] = None
                    else:
                        day1[i] = None

        st_date += datetime.timedelta(days=1)
    return [day0, day1]

    # for week in weeks:
    #     for i in range(6):
    #         if not days[i]:
    #             continue
    #         day = week.days[i]
    #         if day.p1group:
    #             days[i][0] = None
    #         if day.p2group:
    #             days[i][1] = None
    #         if day.p3group:
    #             days[i][2] = None
    #         if day.p4group:
    #             days[i][3] = None
    #         if day.p5group:
    #             days[i][4] = None
    #         if day.p6group:
    #             days[i][5] = None
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
                        day.p2group = group.id
                    if time[0] == 2:
                        day.p3group = group.id
                    if time[0] == 3:
                        day.p4group = group.id
                    if time[0] == 4:
                        day.p5group = group.id
                    if time[0] == 5:
                        day.p6group = group.id
                else:
                    if time[1] == 0:
                        day.p1group = group.id
                    if time[1] == 1:
                        day.p2group = group.id
                    if time[1] == 2:
                        day.p3group = group.id
                    if time[1] == 3:
                        day.p4group = group.id
                    if time[1] == 4:
                        day.p5group = group.id
                    if time[1] == 5:
                        day.p6group = group.id

        st_date += datetime.timedelta(days=1)
    db_sess.commit()
    return True


def get_week_audience(db_sess, audience_id: int, date: datetime.date):
    needed_date = date - datetime.timedelta(days=date.weekday())

    audience = db_sess.query(Audience).filter(Audience.id == audience_id).first()
    if not audience:
        return
    week = db_sess.query(Week).filter(Week.week_start_date == needed_date,
                                      Week.audience_id == audience.id).first()
    if not week:
        create_week(db_sess, needed_date, audience_id)
        week = db_sess.query(Week).filter(Week.week_start_date == needed_date,
                                          Week.audience_id == audience.id).first()
    vweek = vWeek(week.id, week.week_start_date, week.week_end_date, get_audience(audience.id, db_sess),
                  [get_day(dd.id, db_sess) for dd in week.days])
    return vweek


def get_week_group(db_sess, group_id: int, date: datetime.date) -> vWeek:
    group = db_sess.query(Group).filter(Group.id == group_id,
                                        Group.is_mer == False).first()
    if not group:
        return

    audience = db_sess.query(Audience).filter(Audience.id == group.audience_id).first()
    vweek = deepcopy(get_week_audience(db_sess, audience.id, date))
    for day_i in vweek.days:
        for para in range(len(day_i.pars)):
            if not day_i.pars[para]:
                continue
            if day_i.pars[para].id != group_id:
                day_i.pars[para] = None

    return vweek


def get_week_teacher(db_sess, teacher_id: int, date: datetime.date) -> vWeek:
    groups = db_sess.query(Group).filter(Group.teacher_id == teacher_id,
                                         Group.is_mer == False).all()
    if not groups:
        return

    needed_date = date - datetime.timedelta(days=date.weekday())
    audiences = db_sess.query(Audience).filter(Audience.id in [group.audience_id for group in groups]).all()
    weeks = db_sess.query(Week).filter(Week.week_start_date == needed_date,
                                       Week.audience_id in [audience.id for audience in audiences]).all()
    bweek = vWeek(-1, needed_date, needed_date + datetime.timedelta(days=6), -1,
                  [vDay(-1,
                        [None] * 6,
                        -1, needed_date + datetime.timedelta(days=dd), False)
                   for dd in range(7)])

    for day in range(7):
        bweek.days[day].is_holiday = any(week.days[day].is_holiday for week in weeks)
        for para in range(len(bweek.days[day].pars)):
            bweek.days[day].pars[para] = list(filter(lambda x: x is not None, [week.days[day].para_groups[para] for week in weeks]))

    return bweek


def get_group_hours(db_sess, st_date: datetime.date, en_date: datetime.date, group_id):
    week = get_week_group(db_sess, group_id, st_date)
    le = 0
    while st_date <= en_date:
        if st_date.weekday() == 0:
            week = get_week_group(db_sess, group_id, st_date)
        if st_date.weekday() == 6:
            st_date += datetime.timedelta(days=1)
            continue
        day = week.days[st_date.weekday()]
        le += len(list(filter(lambda gr: gr, day.pars)))

        st_date += datetime.timedelta(days=1)
    return le


# db_session.global_init("../../db/GriBD.db")
# le = get_group_hours(db_session.create_session(), st_date=DecodeDate('2023-03-25'), en_date=DecodeDate('2023-04-08'),
#                      group_id=1)
# print(le)
