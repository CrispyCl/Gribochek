import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Day(SqlAlchemyBase):
    __tablename__ = 'days'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    p1group = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    p2group = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    p3group = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    p4group = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    p5group = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    p6group = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    week_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("weeks.id"))
    date = sqlalchemy.Column(sqlalchemy.DATE, nullable=False)
    is_holiday = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)

    week = orm.relationship("Week")
