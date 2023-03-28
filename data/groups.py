import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("users.id"))
    audience_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("audiences.id"))
    need_hours = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    week_day0 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    week_day1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    timeday0 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    timeday1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    course_start_date = sqlalchemy.Column(sqlalchemy.DATE, nullable=True)
    course_end_date = sqlalchemy.Column(sqlalchemy.DATE, nullable=True)

    teacher = orm.relationship('User')
