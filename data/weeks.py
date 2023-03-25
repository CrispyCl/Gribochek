import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Week(SqlAlchemyBase):
    __tablename__ = 'weeks'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    audience_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("audiences.id"))

    days = orm.relationship("Day", back_populates='week')
