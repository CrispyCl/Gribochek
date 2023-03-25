import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class WorkingRate(SqlAlchemyBase):
    __tablename__ = 'working_rates'

    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"),
                                   primary_key=True, nullable=False)
    pars = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    teacher = orm.relationship('User')
