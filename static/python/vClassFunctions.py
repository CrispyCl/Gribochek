from data.days import Day
from data.groups import Group
from data.users import User

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
