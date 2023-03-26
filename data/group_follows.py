import sqlalchemy
from .db_session import SqlAlchemyBase


class GroupFollow(SqlAlchemyBase):
    __tablename__ = 'group_follows'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
