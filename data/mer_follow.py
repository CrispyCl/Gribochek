import sqlalchemy
from .db_session import SqlAlchemyBase


class MerFollow(SqlAlchemyBase):
    __tablename__ = 'mer_follows'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("groups.id"))
    mer_id = sqlalchemy.Column(sqlalchemy.Integer,
                               nullable=False) # groups.id
