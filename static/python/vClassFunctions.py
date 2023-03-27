import datetime

from data.days import Day
from data.groups import Group
from data.users import User
from data.weeks import Week

from static.python.variables import vAudience, vWeek, vDay, vUser, vGroup
from data.audiences import Audience


def get_user(user_id: int, db_sess):
    if db_sess.query(User).filter(User.id == user_id).first():
        user = db_sess.query(User).filter(User.id == user_id).first()
        return vUser(user_id,
                     user.name,
                     user.surname,
                     user.otchestvo,
                     user.email,
                     user.hashed_password,
                     user.img,
                     user.role)


def get_group(group_id: int, db_sess):
    if db_sess.query(Group).filter(Group.id == group_id).first():
        group = db_sess.query(Group).filter(Group.id == group_id).first()
        da_group = vGroup(group_id,
                          group.subject,
                          get_user(group.teacher_id, db_sess),
                          get_audience(group.audience_id, db_sess),
                          group.week_day0,
                          group.week_day1,
                          group.course_start_date,
                          group.course_end_date)
        return da_group


def get_day(day_id: int, db_sess):
    if db_sess.query(Day).filter(Day.id == day_id).first():
        day = db_sess.query(Day).filter(Day.id == day_id).first()
        return vDay(day_id,
                    [get_group(grp, db_sess) for grp in [day.p1group, day.p2group, day.p3group,
                                                         day.p4group, day.p5group, day.p6group]],
                    day.week_id,
                    day.date,
                    day.is_holiday)


def get_audience(audience_id: int, db_sess) -> vAudience:
    if db_sess.query(Audience).filter(Audience.id == audience_id).first():
        audience = db_sess.query(Audience).filter(Audience.id == audience_id).first()
        return vAudience(audience_id, audience.name, audience.image, audience.is_eventable)


def get_week_audience(db_sess, audience_id: int, date: datetime.date):
    needed_date = date - datetime.timedelta(days=date.weekday())
    print(needed_date)

    audience = db_sess.query(Audience).filter(Audience.id == audience_id).first()
    if audience is None and db_sess.query(Week).filter(Week.week_start_date == needed_date,
                                  Week.audience_id == audience.id).first() is None:
        return
    week = db_sess.query(Week).filter(Week.week_start_date == needed_date,
                                      Week.audience_id == audience.id).first()
    vweek = vWeek(week.id, week.week_start_date, week.week_end_date, get_audience(audience.id, db_sess),
                  [get_day(dd.id, db_sess) for dd in week.days])
    return vweek


def get_week_group(db_sess, group_id: int, date: datetime.date) -> vWeek:
    group = db_sess.query(Group).filter(Group.id == group_id).first()
    if not group:
        return

    audience = db_sess.query(Audience).filter(Audience.id == group.audience_id).first()
    bweek = get_week_audience(db_sess, audience.id, date)
    for day_i in bweek.days:
        for para in range(len(day_i.para_groups)):
            if day_i.para_groups[para] is not None and day_i.para_groups[para].id != group_id:
                day_i.para_groups[para] = None

    return bweek


def get_week_teacher(db_sess, teacher_id: int, date: datetime.date) -> vWeek:
    groups = db_sess.query(Group).filter(Group.teacher_id == teacher_id).all()
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
        for para in range(len(bweek.days[day].para_groups)):
            bweek.days[day].para_groups[para] = list(filter(lambda x: x is not None,
                                                            [week.days[day].para_groups[para] for week in weeks]))

    return bweek
