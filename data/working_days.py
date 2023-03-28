import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class WorkingDays(SqlAlchemyBase):
    __tablename__ = 'working_days'

    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"),
                                   primary_key=True, nullable=False)
    days = sqlalchemy.Column(sqlalchemy.String,
                             nullable=False)

    teacher = orm.relationship('User')
