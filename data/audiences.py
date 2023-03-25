import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Audience(SqlAlchemyBase):
    __tablename__ = 'audiences'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # about = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    # images = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # image_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    is_eventable = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)

